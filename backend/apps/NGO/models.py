from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NGO (models.Model):
    NGO_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User,null=True,blank=True,related_name='ngo_profile',on_delete=models.CASCADE)
    name = models.CharField(max_length=50,unique= True)
    address = models.CharField(max_length=250)
    longitude = models.FloatField(null=True,blank=True)
    latitude = models.FloatField(null=True,blank=True)
    category = models.CharField(max_length=10,choices=[('Government','Government'),('Private','Private')],default='Private')
    fcm_token = models.CharField(max_length= 250,null=True,blank=True)
    
    
    
    
    
    def __str__(self):
        return self.name