from django.db import models
from apps.restaurant.models import Restaurant
from apps.NGO.models import NGO
from django.utils import timezone
from datetime import timedelta


#helper for expired_at because lambda not serialized

def expired_time():
    return  timezone.now()+timedelta(minutes=45)

# Create your models here.
class Ticket (models.Model):
    restaurant =models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    food_name= models.CharField(max_length=100)
    category = models.CharField(max_length=10,choices=[('Human','Human'),('Animal','Animal')])
    quantity= models.PositiveIntegerField(default=1)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='ticket_images/',blank=True,null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    is_claimed = models.BooleanField(default=False)
    expired_at = models.DateTimeField(default=expired_time)
    claimed_by= models.ForeignKey(NGO,null=True,blank=True,on_delete=models.SET_NULL,related_name='accepted_tickets')
    STATUS_CHOICES = [
    ('Available', 'Available'),
    ('Reserved', 'Reserved'),
    ('Delivered', 'Delivered'),
    ('Expired', 'Expired'),
]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available')

    
    
    def __str__(self):
        return  f"Ticket from {self.restaurant.name} - {self.food_name}"

    
    def is_expired(self):
        return timezone.now > self.expired_at
    
    
    
    
    def reserved (self,ngo):
        self.claimed_by = ngo
        self.status = 'reserved'
        self.is_claimed = True
        self.expired_at = timezone.now() + timedelta(minutes=45)
        self.save()
    
    def mark_delivered(self):
        self.status = 'Delivered'
        self.save()
        
    def auto_expired(self):
        self.status = ' Expired'
        self.claimed_by= False
        self.is_claimed = None
        self.save()
    
    class Meta:
        ordering =['-created_at']
