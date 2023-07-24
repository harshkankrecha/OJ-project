from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.register,name='register'),
    path('', views.loginuser,name='login'),
    path('logout',views.logoutuser,name='logout'),       
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)