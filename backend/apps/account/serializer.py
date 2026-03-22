from rest_framework import serializers
from.models import User 
from .function.sms_service import send_otp_sms
from .tasks import send_otp_task
from django.conf import settings
import random
from django.core.cache import cache

def generate_otp():
        return str(random.randint(100000 , 999999))
class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    class Meta :
        model = User
        fields = ["phone","role"]
    
    
    def create(self, validated_data): 
        phone = validated_data["phone"]
        role = validated_data["role"]
        
        user,_ = User.objects.get_or_create(
        phone = phone,
        defaults={"role": role}
        )
    
        otp = generate_otp()


# redis me save hoga otp for 5 min 
        cache.set(f"otp:{phone}",otp,timeout=300)
        
        if settings.DEBUG :
            print("OTP_DEBUG",otp)
        else:
        # sms send
            send_otp_task.delay(str(phone),otp)
        return user
        


#VERIFY

class VerifyOtpSerializer(serializers.Serializer):
    phone =serializers.CharField()
    otp = serializers.CharField()
    
    def validate(self, data):
        phone = data.get("phone")
        otp = data.get("otp")
        
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found")

        store_otp = cache.get(f"otp:{phone}")
    
        
        if not store_otp:
            raise serializers.ValidationError("OTP expired")
        if store_otp!= otp.strip():
            raise serializers.ValidationError("OTP invalid")
        cache.delete(f"otp:{phone}")
        data["user"] = user
        return data