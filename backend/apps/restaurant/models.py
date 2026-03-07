from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gis_models

# Create your models here.
class RestaurantProfile(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=200,null=False,blank=False)
    registration_number = models.CharField(max_length=50 , null=False ,blank=False)
    address = models.CharField(max_length=200)
    location = gis_models.PointField(srid=4326 , spatial_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.restaurant_name} {self.user.phone}"