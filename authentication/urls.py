from django.contrib import admin
from django.urls import path,include
from authentication.views import createUser,loginView,LoginAPI,RegisterAPI,forgetPassword


urlpatterns = [
    path('register/', createUser , name='users'),
    path('login/', loginView, name="login"),
    path('login-cl/', LoginAPI.as_view(), name="login-cl"),
    path('register-cl/', RegisterAPI.as_view(), name="register-cl"),
    

    path('forget-password/', forgetPassword, name="forget-password"),
]
