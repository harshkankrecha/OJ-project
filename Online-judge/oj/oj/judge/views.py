from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.views import generic
import os,filecmp
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Problem,Solution
from django.shortcuts import render,redirect

def home(request):
    #if request.user.is_anonymous:
    #    return redirect("/login")
    return render(request,'home.html')

def problems(request):
    problems_list=Problem.objects.all()
    context={'problems_list':problems_list}
    return render(request,'index.html',context)

def problemDetail(request,problem_id):
    problem=get_object_or_404(Problem,pk=problem_id)
    return render(request,'detail.html',{'problem':problem})

def submitProblem(request,problem_id):
    f=request.FILES['solution']
    with open('/Users/harsh/Desktop/Project2/oj/oj/static/solution.py','wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    os.system('/Users/harsh/Desktop/Project2/oj/oj/static/solution.py')
    os.system('python </Users/harsh/Desktop/Project2/oj/oj/static/./solution.py> /Users/harsh/Desktop/Project2/oj/oj/static/out.txt')

    out1='/Users/harsh/Desktop/Project2/oj/oj/static/out.txt'
    out2='/Users/harsh/Desktop/Project2/oj/oj/static/actual_out.txt'

    f1 = open("/Users/harsh/Desktop/Project2/oj/oj/static/out.txt", "r")  
    f2 = open("/Users/harsh/Desktop/Project2/oj/oj/static/actual_out.txt", "r")  
  
    i = 0
    flag=0
    for line1 in f1:
        i += 1
        
        for line2 in f2:
            
            # matching line1 from both files
            if line1 != line2:  
                verdict='wronganswer.html'
                flag=1                    
                break
        if flag==1:
            break
    if flag==0:
        verdict="accepted.html"
        
    
    # closing files
    f1.close()                                       
    f2.close()      

    

    solution=Solution()
    solution.problem=Problem.objects.get(pk=problem_id)
    solution.verdict=verdict
    solution.submitted_at=timezone.now()
    solution.submitted_code='/Users/harsh/Desktop/Project2/oj/oj/static/solution.py'
    solution.save()

    return render(request,verdict)

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

def leaderboard(request):
    solutions=Solution.objects.all()
    return render(request,'leaderboard.html',{'solutions':solutions})


