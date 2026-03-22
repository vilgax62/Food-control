from rest_framework import viewsets  
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework.permissions import IsAuthenticated
from .models import Donation
from .serializer import DonationSerializer
from apps.Restaurant.models import RestaurantProfile
from apps.NGO.models import NGOProfile
from django.db import transaction
from backend.utils.notification import send_ws_notification
from rest_framework.exceptions import PermissionDenied
from backend.utils.fcm import send_push_notification
class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class=DonationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if hasattr(user,"restaurant"):
            return Donation.objects.filter(donated_by__user=user)
        if hasattr(user,"ngoprofile"):
            return Donation.objects.filter(status= "PENDING")
        return Donation.objects.none()
    def perform_create(self, serializer):
        if not hasattr(self.request.user,"restaurantprofile"):
            raise PermissionDenied("Only restaurant can create donation")
        restaurant = RestaurantProfile.objects.get(user=self.request.user)
        donation   = serializer.save(donated_by = restaurant,status="PENDING")
        # notification alert
        ngos = NGOProfile.objects.filter(location__distance_lte=(restaurant.location,D(km=15)))
        for ngo in ngos :
            send_ws_notification(ngo.user.id,"New food donation available",{
                "donation_id":donation.id
                })
            if ngo.user.fcm_token:
                send_push_notification(ngo.user.fcm_token,"New food","Food available near you",{"donation_id":str(donation.id)})
        
        
    @action(detail=False,methods=["get"])
    def nearby(self,request):
        ngo = NGOProfile.objects.get(user=request.user)
        ngo_location = ngo.location
        donations = Donation.objects.filter(status="PENDING",is_active= True,donated_by__location__distance_lte=
                (ngo_location,D(km=15))).annotate(distance = Distance("donated_by__location",ngo_location)).order_by("distance")
        serializer = self.get_serializer(donations,many=True)
        return Response(serializer.data)
    
    
    @action(detail=True,methods=["post"])
    def accept(self,request,pk=None):
        
            if not hasattr(request.user,"ngoprofile",None):
                return Response ({"error":"Only NGO can accept donation"})
            with transaction.atomic():
                donation = self.get_object()
        # expired
            if donation.is_expired():
                return Response ({"error":"Donation expired"},status=400)
            ngo = NGOProfile.objects.get(user=request.user)
            if donation.status != "PENDING":
                return Response({"error":"Donation already accepted"})
            donation.accepted_by = ngo
            donation.status = "ACCEPTED"
            donation.save()
            
            send_ws_notification(donation.donated_by.user.id,"your donation accepted",{
            "donation_id":donation.id})
            
            if donation.donated_by.user.fcm_token:
                send_push_notification(donation.donated_by.user.fcm_token,"donation accepted","Ngo accepted your food",{"donation_id":str(donation.id)})
        
            return Response ({"message":"Donation accepted"})
    
    
    @action(detail=True,methods=["post"])
    def pickup(self,request,pk=None):
        donation = self.get_object()
        if donation.status != "ACCEPTED":
            return Response({"error":"Donation not accepted yet"})
        if donation.accepted_by.user != request.user:
            return Response ({"error":"Not your donation"})
        donation.status = "PICKED_UP"
        donation.save()
        return Response ({'message':"Food picked up"})
    
    
    @action(detail=True,methods=["post"])
    def deliver(self,request,pk=None):
        donation = self.get_object()
        if not donation.status == "PICKED_UP":
            return Response ({"error":"Food not picked yet"})
        donation.status = "DELIVERED"
        donation.is_active = False
        donation.save()
        return Response({"message":"Food delivered"})
        