from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
# Create your views here.

def register(request):
    if request.method=='POST':
        first_name=request.post('first_name')
        last_name=request.post('last_name')
        username=request.post('username')
        password1=request.post('password1')
        password2=request.post('password2')

        user=User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name)
        user.save()
        return redirect("/")
    else:
        return render(request,'register.html')