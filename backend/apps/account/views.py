from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializer import RegisterSerializer ,VerifyOtpSerializer
from .function.service import get_token_for_user
from .function.RateLimit import RateLimit
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view


##LOGIN
class  SendOtpView(APIView):
    throttle_classes = [RateLimit]
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


##LOGOUT
class LogoutView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message":"Logout successful"},
                status= status.HTTP_200_OK
            )
        except:
            return Response(
                {"error":"Invalid token"},
                status= status.HTTP_400_BAD_REQUEST
            )


#fcm push notification 

@api_view(["POST"])
def save_fcm_token(request):
    user = request.user
    token = request.data.get("token")
    user.fcm_token  = token
    user.save()
    return Response({"message":"token saved"})
