from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('problems',views.problems, name='problems'),
    path('',views.loginuser, name='login'),
    path('logout',views.logoutuser, name='logout'),
    path('submit',views.submit,name='submit')
]

admin.site.site_header = "Codehelp Admin"
admin.site.index_title = "Welcome to Codehelp"
admin.site.site_title = "Codehelp"