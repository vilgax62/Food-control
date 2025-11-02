from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.NGO.models import NGO
from apps.restaurant.models import Restaurant
from apps.ticket.models import Ticket
from apps.restaurant.serializers import Restaurantserializers
from apps.NGO.serializers import NGOserializers
from  apps.ticket.utils import distance_km





@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def restaurant_list_create(request):
    # user = request.user  

    
    if  request.method == 'GET' :
        rest_lat = float(request.GET.get('latitude'))
        rest_lon = float(request.GET.get('longitude'))
        
        nearby_ngos= [
            n for n in NGO.objects.all()
            if distance_km(rest_lat,rest_lon, n.latitude, n.longitude) <=15
        ]
        serializer = NGOserializers(nearby_ngos ,many = True)
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        # ✅ Fetch the existing restaurant (based on logged-in user or id)
        restaurant_id = request.data.get('id')  # or fetch via user if using JWT
        if not restaurant_id:
            return Response({'error': 'Restaurant id is required for update'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Pass instance + data
        serializer = Restaurantserializers(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def ticket_mark_delivered(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)

    if ticket.status != "Reserved":
        return Response({'error': 'Ticket must be Reserved before marking delivered'}, status=status.HTTP_400_BAD_REQUEST)

    ticket.mark_delivered()
    return Response({'message': 'Ticket marked as Delivered successfully'})