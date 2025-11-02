from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Restaurant (models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,null=True,blank=True,related_name='restaurant_profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    address= models.CharField(max_length=250)
    category = models.CharField(max_length=6, choices=[('Human','Human'),
            ('Animal','Animal'),],default='Human')
    latitude = models.FloatField(null=True,blank=True)
    longitude = models.FloatField(null=True,blank=True)
    image= models.ImageField(upload_to='restaurant_images/',blank=True,null=True)
    
    def __str__(self):
        return self.name