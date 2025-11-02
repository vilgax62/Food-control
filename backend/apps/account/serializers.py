from rest_framework import serializers
from django.contrib.auth.models import User
from apps.NGO.models import NGO
from apps.restaurant.models import Restaurant



class NGOsignupserializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    password = serializers.CharField(write_only = True)
    
    
    class Meta :
        model = NGO
        fields = ['username', 'email', 'password', 'name', ]
        
    def create(self, validated_data):
        username = 'ngo_'+ validated_data.pop('username').lower()
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username,password=password,email=email)
        ngo = NGO.objects.create(user= user,**validated_data)
        return ngo
    
    

class restsignupserializers(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    email = serializers.EmailField(write_only = True)
    password = serializers.CharField(write_only = True)
    
    
    class Meta:
        model = Restaurant
        fields = ['username', 'email', 'password', 'name',]
        
        
    def create(self, validated_data):
        username = 'rest_'+ validated_data.pop('username').lower()
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username,email=email,password=password)
        rest = Restaurant.objects.create(user=user,**validated_data)
        
        return rest
    

class loginserializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()