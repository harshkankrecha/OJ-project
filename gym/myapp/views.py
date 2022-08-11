from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import User,Queries
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        mobile_number=request.POST['mobile_number']
        user_message=request.POST['user_message']
        query=Queries(first_name=first_name,last_name=last_name,mobile_number=mobile_number,user_message=user_message)
        query.save()
        messages.error(request,'Your message has been received successfully.')
    return render(request,'home.html')

def subscription(request):
    return render(request,'subscribe.html')

def register(request):
    
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        cweight=request.POST['cweight']
        gweight=request.POST['gweight']
        bmi=request.POST['bmi']
        gender=request.POST['gender']
        age=request.POST['age']
        address=request.POST['address']
        
        if len(first_name)==0:
            messages.error(request,'First Name cannot be empty')
            return render(request,'register.html')
        elif len(cweight)==0 or len(gweight)==0:
            messages.error(request,'Weight should not be empty')
            return render(request,'register.html')
        elif len(age)==0:
            messages.error(request,'Age should not be empty')
            return render(request,'register.html')
        elif len(gender)==0:
            messages.error(request,'Gender should not be empty')
            return render(request,'register.html')
        elif len(bmi)==0:
            messages.error(request,'BMI should not be empty')
            return render(request,'register.html')
        elif len(email)==0:
            messages.error(request,'Email should not be empty')
            return render(request,'register.html')

        elif len(address)==0:
            messages.error(request,'Address Name cannot be empty')
            return render(request,'register.html')
        else:
            if User.objects.filter(email=email).exists():
                return redirect('subscription')
            else:
                user=User(first_name=first_name,last_name=last_name,email=email,current_weight=int(cweight),goal_weight=int(gweight),bmi=float(bmi),gender=gender,age=int(age),address=address)
                user.save()
                return redirect('subscription')
                
            
                


        
            
            
                
        
    else:
        return render(request,'register.html')
