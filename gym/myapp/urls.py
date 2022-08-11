from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('subscription', views.subscription, name='subscription'),    
    path('register', views.register, name='register'),

]