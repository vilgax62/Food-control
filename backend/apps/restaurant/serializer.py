from rest_framework import serializers
from .models import RestaurantProfile


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model =RestaurantProfile
        fields ="__all__"
        read_only_fields =["user","created_by","updated_by"]