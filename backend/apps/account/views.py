from rest_framework import status
from rest_framework.response import Response
from .serializers import loginserializers,NGOsignupserializer,restsignupserializers
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



@ api_view(['POST'])
def ngo_register(request):
    serializer = NGOsignupserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message : Ngo registered successfully'} ,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def rest_register(request):
    serializer = restsignupserializers(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message : Restaurant registered successfully'} ,status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def login_view(request):
    serializer = loginserializers(data=request.data)
    if serializer.is_valid():
        username =  serializer.validated_data['username']
        password = serializer.validated_data[('password')]
        
        
        user = authenticate(username= username, password= password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_type = (
                "NGO"
                if username.startswith("ngo_")
                else "Restaurant"
                if username.startswith("rest_")
                else "unknown"
            )
            return Response({
                'access' : str(refresh.access_token),
                'refresh' : str(refresh),
                'type' :   user_type,
                'username' : user.username
            }, status= status.HTTP_200_OK)
        return Response({'error': "invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            