from rest_framework import serializers 
from rest_framework_simplejwt import serializers as jwt_serializers 
from core.models import Note,CustomUser 
from django.contrib.auth import get_user_model

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields = ("name","email", "password")
    
    def save(self):
        user=get_user_model()(
            name=self.validated_data["name"],
            email=self.validated_data["email"],
        )
        password = self.validated_data["password"]

        user.set_password(password)
        user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    email=serializers.EmailField()
    
    def validate(self, attrs):
        email=attrs["email"]
        try:
            user=get_user_model().objects.get(email=email)
            return user
        except Exception as e:
            raise serializers.ValidationError({"email":"Email is not registered"})
        
        
    
        
class MyTokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.name
        return token

