from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from apps.ticket.utils import distance_km
from apps.restaurant.models import Restaurant
from apps.restaurant.serializers import Restaurantserializers
from apps.NGO.serializers import NGOserializers
from apps.NGO.models import NGO

@api_view(['GET','PATCH'])
def ngo_list(request):
    
    if request.method == 'GET':
        # Get latitude and longitude safely
        lat = request.GET.get('latitude')
        lon = request.GET.get('longitude')

        if lat is None or lon is None:
            return Response(
                {'error': 'latitude and longitude query parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response(
                {'error': 'latitude and longitude must be valid numbers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        nearby_restaurant= [
            n for n in Restaurant.objects.all()
            if distance_km(lat,lon, n.latitude, n.longitude) <=15
        ]
        serializer = Restaurantserializers(nearby_restaurant ,many = True)
        return Response(serializer.data)
    
    elif request.method == 'PATCH' :
        
        ngo_id = request.get.id('id')
        if not ngo_id:
            return Response({'error': 'NGO id is required for update'},status=status.HTTP_401_UNAUTHORIZED)
        try:
            ngo = NGO.objects.get(ngo_id=ngo_id)
        except NGO.DoesNotExist:
            return Response ({'error': 'NGO data is not found '},status=status.HTTP_400_BAD_REQUEST)
        serializer = NGOserializers(ngo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
    
