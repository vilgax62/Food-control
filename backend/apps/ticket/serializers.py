from rest_framework import serializers
from .models import Ticket



class Ticketserializers(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['is_claimed', 'expired_at', 'created_at', 'status']