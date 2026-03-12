from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta :
        model = Donation
        fields = "__all__"
        read_only_fields = ["accepted_by","status","created_by","updated_by"]