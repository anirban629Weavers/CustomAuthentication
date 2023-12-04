from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from core.manager import UserManager


class CustomUser(AbstractBaseUser):
    email = models.EmailField(null=False, blank=False, unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    password=models.CharField(max_length=45)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class Note(models.Model):
    author=models.ForeignKey(CustomUser,related_name="Note_Owner",on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=50,default="Default Title")
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PasswordToken(models.Model):
    user=models.ForeignKey(CustomUser,related_name="Password_token",on_delete=models.CASCADE,null=True)
    token=models.CharField(max_length=15,default="0")