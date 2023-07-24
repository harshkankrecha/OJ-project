from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'*Username already taken*')
                return render(request,'register.html')
            else:
                user=User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('/')
                
        else:
            messages.error(request,'*Password not matching*')
            return render(request,'register.html')
    else:
        return render(request,'register.html')

def loginuser(request):
    if request.method=="POST" and 'first_name' in request.POST:            
        first_name=request.POST['first_name']
        #print(first_name)
        last_name=request.POST['last_name']
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'*Username already taken*')
                return render(request,'login2.html')
            else:
                user=User.objects.create_user(username=username,password=password1,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('/')                
        else:
            messages.error(request,'*Password not matching*')
            return render(request,'login2.html')
    elif request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/judge')
        else:
            messages.error(request,'*Invalid credentials*')
            return render(request,"login2.html")
    else:
        return render(request,'login2.html')
            
def logoutuser(request):
    logout(request)
    request.session.flush()
    request.session.clear_expired()
    return redirect('/')

