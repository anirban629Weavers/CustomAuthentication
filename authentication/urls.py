from django.contrib import admin
from django.urls import path,include
from authentication.views import createUser,loginView


urlpatterns = [
    path('register/', createUser , name='users'),
    path('login/', loginView, name="login"),
]
