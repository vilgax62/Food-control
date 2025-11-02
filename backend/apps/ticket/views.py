from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.ticket.models import Ticket
from apps.ticket.serializers import Ticketserializers
from apps.NGO.models import NGO
from apps.ticket.utils import distance_km
from firebase_admin import messaging



@api_view(['GET','POST'])
def ticket_create(request):
    
    if  request.method == 'GET' :
        ngo_lat = float(request.GET.get('latitude'))
        ngo_lon = float(request.GET.get('longitude'))
        
        tickets=[]
        for t in Ticket.objects.select_related('restaurant').all():
            if distance_km(ngo_lat,ngo_lon,t.restaurant.latitude,t.restaurant.longitude) <= 15 :
                tickets.append(t)
            
        serializer = Ticketserializers(tickets, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST' :
        serializer = Ticketserializers(data = request.data)
        if serializer.is_valid():
            ticket = serializer.save()
            
            
            rest = ticket.restaurant
            nearby_ngos= [
            n for n in NGO.objects.all()
            if distance_km(rest.latitude, rest.longitude,n.latitude,n.longitude) <=15
        ]
            
            for ngo in nearby_ngos:
                if ngo.fcm_token :
                    message = messaging.Message(
                        notification = messaging.Notification(
                            message = "New food is available",
                            body = (f"{rest.name} has created a food ticket {ticket.food_name}")
                        ),
                        token = ngo.fcm_token,
                    )
                    messaging.send(message)
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def ticket_update_status(request,ticket_id):
    try:
        ticket = Ticket.objects.get(id = ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error ' :'Ticket not found'} ,status=status.HTTP_404_NOT_FOUND)
    
    ngo_id = request.data.get('ngo_id')
    if not ngo_id:
        return Response({'error': 'NGO_id required'}, status=status.HTTP_400_BAD_REQUEST)

    from apps.NGO.models import NGO
    try:
        ngo = NGO.objects.get(NGO_id=ngo_id)
    except NGO.DoesNotExist:
        return Response({'error': 'NGO not found'}, status=status.HTTP_404_NOT_FOUND)

    # Assign ticket
    if ticket.status == "Available":
        ticket.reserved(ngo)
        return Response({'message': 'Ticket reserved by NGO successfully'})
    else:
        return Response({'error': f'Ticket not available (currently {ticket.status})'})

