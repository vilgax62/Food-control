from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.Restaurant.models import RestaurantProfile
from apps.NGO.models import NGOProfile


# Create your models here.

#core description
class Donation(models.Model):
    donated_by = models.ForeignKey(RestaurantProfile,on_delete=models.CASCADE,related_name="donations")
    accepted_by = models.ForeignKey(NGOProfile,on_delete= models.SET_NULL,null=True,blank=True ,related_name="accept_donation")
    accepted_by
    STATUS_CHOICE = (('PENDING','Pending'),
                    ('ACCEPTED','Accepted'),
                    ('PICKED_UP','Pick up'),
                    ('DELIVERED','Delivered'),
                    ('CANCELLED','Cancelled'),
                    ("EXPIRED", "Expired"),)
    status = models.CharField(max_length=20,choices=STATUS_CHOICE,default="PENDING")
    FOOD_TYPE = (('VEG','Veg'),('NON_VEG','Non veg'))
    food_type =models.CharField(max_length=20,choices=FOOD_TYPE)
    food_description = models.TextField()
    quantity = models.CharField(max_length=100)
    pickup_time = models.DateTimeField()
    expiry_time = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="donations/",null=True,blank=True)
    notes = models.TextField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    
#dynamic calculation
    search_radius = models.IntegerField(default=15)
    radius_increment = models.IntegerField(default=5)
    max_radius = models.IntegerField(default=50)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["search_radius"]),
            models.Index(fields=["expiry_time"]),
        ]
    def save(self, *args, **kwargs):
        if not self.expiry_time:
            self.expiry_time = timezone.now() + timedelta(minutes= 45)
        super().save(*args,**kwargs)
    def clean(self):
        if self.status == "ACCEPTED" and not self.accepted_by:
            raise ValidationError("Accepted donation must have a NGO assigned")
        if self.accepted_by and self.status != "ACCEPTED":
            raise ValidationError("Cannot assign NGO while status is still pending")
    
    def can_transition(self, new_status):
        transitions = {
            "PENDING": ["ACCEPTED", "CANCELLED", "EXPIRED"],
            "ACCEPTED": ["PICKED_UP", "CANCELLED"],
            "PICKED_UP": ["DELIVERED"],
            "DELIVERED": [],
            "CANCELLED": [],
            "EXPIRED": [],
        }
        return new_status in transitions.get(self.status, [])
    
    def is_expired(self):
            if self.expiry_time:
                return timezone.now() > self.expiry_time
            return False

    def extend_radius(self):
        if self.search_radius < self.max_radius:
            self.search_radius += self.radius_increment
            self.expiry_time = timezone.now() + timedelta(minutes=30)
            self.save()
            return "extended"
        else:
            self.status = "EXPIRED"
            self.is_active = False
            self.save()
            return "expired"
    
    
    def __str__(self):
        return f"{self.donated_by.restaurant_name} - {self.status}"