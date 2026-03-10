from rest_framework import viewsets  
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import point
from django.contrib.gis.measure import D
from rest_framework.permissions import IsAuthenticated
from .models import Donation
from .serializer import DonationSerializer
from apps.Restaurant.models import RestaurantProfile
from apps.NGO.models import NGOProfile



class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class=DonationSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        restaurant = RestaurantProfile.objects.get(user=self.request.user)
        serializer.save(donated_by = restaurant,status="PENDING")
        
    @action(detail=False,methods=["get"])
    def nearby(self,request):
        ngo = NGOProfile.objects.get(user=request.user)
        ngo_location = ngo.location
        donations = Donation.objects.filter(status="PENDING",is_active= True,donated_by__location__distance_lte=(ngo_location,D(km=15))).annotate(distance = Distance("donated_by__location",ngo_location)).order_by("distance")
        # expiry
        for donation in donations:
            if donation.is_expired():
                donation.extend_radius()
        serializer = self.get_serializer(donations,many= True)
        
        return Response(serializer.data)
    
    
    @action(detail=True,methods=["post"])
    def accept(self,request,pk=None):
        donation = self.get_object()
        # expied
        if donation.is_expired():
            donation.extend_radius()
            return Response ({"error":"Donation expired"})
        ngo = NGOProfile.objects.get(user=request.user)
        if donation.status != "PENDING":
            return Response({"error":"Donation already accepted"})
        donation.accepted_by = ngo
        donation.status = "ACCEPTED"
        donation.save()
        
        return Response ({"message":"Donation accepted"})
    
    
    @action(detail=True,methods=["post"])
    def pickup(self,request,pk=None):
        donation = self.get_object()
        if donation.status != "ACCEPTED":
            return Response({"error":"Donation not accepted yet"})
        donation.status = "PICKED_UP"
        donation.save()
        return Response ({'message':"Food picked up"})
    
    
    @action(detail=True,methods=["post"])
    def deliver(self,request):
        donation = self.get_object()
        if not donation.status == "PICKED_UP":
            return Response ({"error":"Food not picked yet"})
        donation.status = "DELIVERED"
        donation.save()
        return Response({"message":"Food delivered"})
        