from rest_framework import serializers
from .models import NGO


class NGOserializers(serializers.ModelSerializer):
    class Meta :
        model = NGO
        fields ='__all__'