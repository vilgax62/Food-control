from rest_framework import serializers
from.models import User , OTP

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
    
        otp_obj,_= OTP.objects.get_or_create(user=user)
        otp_obj.generate_otp()
        
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
        try:
            otp_obj = OTP.objects.get(user=user)
        except OTP.DoesNotExist:
            raise serializers.ValidationError("OTP not generated")
        
        if otp_obj.expired():
            otp_obj.delete()
            raise serializers.ValidationError("OTP expired")
        if otp_obj.otp != otp.strip():
            raise serializers.ValidationError("OTP invalid")
        otp_obj.delete()
        data["user"] = user
        return data