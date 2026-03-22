from rest_framework import serializers
from .models import NGOProfile


class NGOSerializer(serializers.ModelSerializer):
    class Meta :
        model = NGOProfile
        fields = "__all__"
        read_only_fields =["user","created_by","updated_by"]