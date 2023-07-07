from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register', views.register,name='register'),
    path('', views.loginuser,name='login'),
    path('logout',views.logoutuser,name='logout'),       
]