from django.shortcuts import render,redirect,HttpResponse
from .models import Subscriber
from myapp.models import User
import stripe
from django.views.decorators.csrf import csrf_exempt

gfirst_name=''
glast_name=''
gplan_price=0
gplan_name=''
def payment(request):   
    global gfirst_name,gplan_price,glast_name,gplan_name    
    if request.method=="POST":
        plan_name=request.POST['plan_name']
        last_entry=User.objects.latest('date')
        first_name=last_entry.first_name
        last_name=last_entry.last_name
        plan_price=0
        
        if plan_name=='basic':
            plan_price=1499
        elif plan_name=='premium':
            plan_price=2199
        else:
            plan_price=3599
        gfirst_name=first_name
        glast_name=last_name
        gplan_name=plan_name
        gplan_price=plan_price      

        
    
    
    return render(request,'payment.html',{'plan_name':plan_name,'plan_price':plan_price,'first_name':first_name,'plan_price2':plan_price*100})
@csrf_exempt
def success(request):
    if request.method=="POST":
        subscriber=Subscriber(first_name=gfirst_name,last_name=glast_name,plan_name=gplan_name,plan_price=gplan_price)
        subscriber.save()
        return render(request, "success.html")
    return redirect('/')
