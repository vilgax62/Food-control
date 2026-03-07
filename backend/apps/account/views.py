from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer ,VerifyOtpSerializer
from .service import get_token_for_user


class  SendOtpView(APIView):
    def post (self,request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {"message" : "OTP sent successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#VERIFY_OTP:
class VerifyOtpView(APIView):
    def post(self,request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens= get_token_for_user(user)
            return Response(
                {"message" : "OTP verified successfully ",
                "phone" : str(user.phone),
                "role" : user.role,
                "tokens": tokens },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
