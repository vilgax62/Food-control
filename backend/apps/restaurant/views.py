from rest_framework import viewsets
from .serializer import RestaurantSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RestaurantProfile

# Create your views here.

class RestaurantProfileViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    
    #restaurant can only there profile / only logged user profile can see
    def get_queryset(self):
        return RestaurantProfile.objects.filter(user = self.request.data)
    
    #extra attachment like user logged in profile 
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)