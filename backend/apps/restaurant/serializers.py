from rest_framework import serializers
from .models import Restaurant

class Restaurantserializers(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields =['restaurant_id','name','category','latitude','longitude','image']