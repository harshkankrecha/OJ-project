from django.shortcuts import render,HttpResponse,redirect
from home.models import Questions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'index.html')

def problems(request):
    data = Questions.objects.all()
    que = {
    "question_number": data
    }
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,"problems.html", que)

def submit(request):
    
    return render(request,'form.html')
    
    #return render(request,'problems.html')

def loginuser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            messages.error(request,'Username or Password is not correct')
            return render(request,"login.html")
    else:
        return render(request,"login.html")

    

def logoutuser(request):
    logout(request)
    return render(request,"login.html")