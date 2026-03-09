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
    
    USERNAME_FIELD ='phone'
    REQUIRED_FIELDS =[]
    
    def __str__(self):
        return str(self.phone)
    
    
    
#OTP
class OTP(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def generate_otp(self):
        self.otp = str(random.randint(100000 , 999999))
        self.created_at=timezone.now()
        self.save()
    
    def expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)
    
