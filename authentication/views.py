from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import tokens
from rest_framework import exceptions as rest_exceptions,response,generics
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from core.serializers import LoginSerializer,RegistrationSerializer,ForgotPasswordSerializer
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from rest_framework import  status

def get_user_tokens(user):
    refresh = tokens.RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

class LoginAPI(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    permission_classes=[AllowAny]
    throttle_scope = 'custom'

class RegisterAPI(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=RegistrationSerializer
    
                
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

@permission_classes([AllowAny])
def createUser(request):
    serailizer=RegistrationSerializer(data=request.data)
    serailizer.is_valid(raise_exception=True)
    
    user=serailizer.save()
    
    if user is not None:
        return response.Response("User Registered Successfully")
    else: raise rest_exceptions.ParseError("Invalid Token")    


@csrf_exempt
@api_view(["POST"])
def forgetPassword(request):
    serializer=ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        msgLink=f'/forget-'
        return response.Response({"msg-link":msgLink},status=status.HTTP_200_OK)