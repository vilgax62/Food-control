from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
import random
from django.conf import settings


# Create your models here.

#user
class User(AbstractUser):
    username = None
    phone = PhoneNumberField("Phone Number ", region = "IN",unique=True,)
    ROLE_CHOICE=(('ADMIN','Admin'),
                ('NGO','Ngo'),
                ('RESTAURANT','Restaurant'))
    role = models.CharField(max_length=20,choices=ROLE_CHOICE,default= 'NGO')
    fcm_token = models.TextField(null= True,blank=True)
    
    USERNAME_FIELD ='phone'
    REQUIRED_FIELDS =[]
    
    def __str__(self):
        return str(self.phone)
    
    
    

