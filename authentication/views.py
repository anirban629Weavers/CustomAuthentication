from django.contrib.auth import authenticate
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from core.models import CustomUser
from core.serializers import UserSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt import tokens,serializers
from rest_framework import exceptions as rest_exceptions,response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from core.serializers import LoginSerializer,RegistrationSerializer

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def loginView(request):
    serializer=LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)    

    email=serializer.validated_data['email']
    password=serializer.validated_data['password']

    try:
        user=authenticate(email=email, password=password)
        res=get_user_tokens(user)
        return response.Response(res)
    except Exception as e:
        raise rest_exceptions.AuthenticationFailed("Invalid Credentials")

@api_view(["POST"])
@permission_classes([AllowAny])
def createUser(request):
    serailizer=RegistrationSerializer(data=request.data)
    serailizer.is_valid(raise_exception=True)
    
    user=serailizer.save()
    
    if user is not None:
        return response.Response("User Registered Successfully")
    else: raise rest_exceptions.ParseError("Invalid Token")    



