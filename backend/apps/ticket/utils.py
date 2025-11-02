import math 


def distance_km(lat1,lon1,lat2,lon2):
    R = 6371
    dlat = math.radians(lat2-lat1)
    dlon= math.radians(lon2-lon1)
    
    a = (
        math.sin(dlat/2) **2 +
        math.cos(math.radians(lat1))*
        math.cos(math.radians(lat2)) *
        math.sin(dlon/2)**2
    )
    
    c = 2* math.atan2(math.sqrt(a),math.sqrt(1-a))
    return R*c

from django.utils import timezone
from apps.ticket.models import Ticket

def expire_old_tickets():
    now = timezone.now()
    expired_tickets = Ticket.objects.filter(status='Reserved', expired_at__lt=now)
    for ticket in expired_tickets:
        ticket.auto_expire()
