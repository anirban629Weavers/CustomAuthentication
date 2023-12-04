from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import tokens
from rest_framework import exceptions as rest_exceptions,response,generics
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from core.serializers import LoginSerializer,RegistrationSerializer,ForgotPasswordSerializer,ForgotPasswordDataSerializer
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import get_user_model 
from rest_framework import  status
from django.core.mail import send_mail
import string,random
from core.models import PasswordToken

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

def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(15))
    if PasswordToken.objects.filter(token=random_string).exists():
        generate_random_string()
        
    return random_string

@csrf_exempt
@api_view(["POST"])
def forgetPassword(request):
    serializer=ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        try:
            token=generate_random_string()
            PasswordToken.objects.create(user=serializer.validated_data,token=token)
            link=f"/user/{token}"
            send_mail(
                    'Forgot Password',
                    f'''
                        Hi {serializer.validated_data},

                        There was a request to change your password!

                        If you did not make this request then please ignore this email.

                        Otherwise, please click this link to change your password: {link}
                    ''',
                    'arnab.gupta@weavers-web.com',
                    ['anirban@yopmail.com'],
                    fail_silently=False,
                )
            return response.Response(
                    {"msg":"If a user with this mail exists, then Message is Sent Successfully"},
                    status=status.HTTP_200_OK   
                )
        except Exception as e:
            print(e)
            return response.Response({"msg":"Failed to send message"})



@csrf_exempt
@api_view(["POST"])       
def forgetPasswordToken(request,id):
    if PasswordToken.objects.filter(token=id).exists():
        serializer=ForgotPasswordDataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:                
                currentUser=PasswordToken.objects.filter(token=id).first().user
                updatedPassword=serializer.validated_data.get("password")
                currentUser.delete()
                currentUser.set_password(updatedPassword)
                currentUser.save()
                return response.Response({"msg":"Password has been updated successfully"})
            except Exception as e:
                print(e)
                return response.Response({"msg":"Some error Occurred"})     
    else:
        print("Invalid token")
        
    return response.Response({"msg":"Link Expired"})
