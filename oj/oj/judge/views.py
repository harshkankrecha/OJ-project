from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse,QueryDict
from django.utils import timezone
from django.urls import reverse
from django.views import generic
import os,filecmp,subprocess
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Problem,Solution,Testcases
from django.shortcuts import render,redirect
from pathlib import Path
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from collections import deque
import json
from .task import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def compare_text_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    # Compare the lines
    if len(lines1) != len(lines2):
        return False

    for line1, line2 in zip(lines1, lines2):
        if line1.strip() != line2.strip():
            return False

    return True
def timeout_handler():
    flag=-2
    raise TimeoutError

# Provide the paths to the text files

def home(request):
    #if request.user.is_anonymous:
    #    return redirect("/login")
    #process_uploaded_file.delay()
    #return HttpResponse("this is the home page")
    return render(request,'home.html')


def problems(request):
    problems_list=Problem.objects.all()
    context={'problems_list':problems_list}
    return render(request,'index.html',context)


def problemDetail(request,problem_id):
    problem=get_object_or_404(Problem,pk=problem_id)
    return render(request,'detail.html',{'problem':problem,'problem_id':problem_id})

def submitProblem(request,problem_id):
    f=request.FILES['solution']
   
    with open(str(BASE_DIR) + '/static/solution.py','wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    flag=count=1
    python_file_path = str(BASE_DIR) + '/static/solution.py'
    problem=get_object_or_404(Problem,pk=problem_id)
    test_data = Testcases.objects.filter(problem=problem)
    timeout = 5    
    
    for testcase in test_data:     
        #=  str(BASE_DIR) + '/static/input.txt'
        #=  str(BASE_DIR) + '/static/answer.txt'  
        input_file_path=str(BASE_DIR) + '/'+str(testcase.input_file)
        answer_file_path=str(BASE_DIR) + '/'+str(testcase.answer_file)
        with open(input_file_path, 'r') as file:
            input_data = file.read()  
        
               
        # Run the Python file and pass the input from the text file
        try:            
            process = subprocess.Popen(['python', python_file_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output, error = process.communicate(input=input_data,timeout=timeout)
                     
        
        except subprocess.TimeoutExpired:
            process.kill()  # Terminate the process if it exceeds the timeout
            process.communicate()      
            flag=-2
            verdict=f"Time limit exceeded on testcase {count}"
            message="Time Limit Exceeded"
            break
        if flag==-2:
            break
        # Store the output in a text file
        output_file_path = str(BASE_DIR) + '/static/output.txt'
        with open(output_file_path, 'w') as file:
            file.write(output)   

        if error:  
            flag=-1       
            error_type = (error.split('^')[1].strip()).split(':')[0]
            if error_type=="SyntaxError":
                verdict=f"Compilation Error on testcase {count}"
                
            else:
                verdict=f"Runtime Error on testcase {count}"
                
            break
            #print(f'An error occurred:')
            
        else:
            result=compare_text_files(output_file_path,answer_file_path)   
            if not result:
                flag=0
                break
            count+=1 
    
              
    
    
    if flag==1:
        verdict="Accepted"
        
    elif flag==0:
        verdict=f"Wrong Answer on testcase {count}"
    
            
    
    solution=Solution()
    solution.user=request.user
    solution.problem=Problem.objects.get(pk=problem_id)
    solution.verdict=verdict
    solution.submitted_at=timezone.now()
    solution.submitted_code=python_file_path
    #solution.submitted_code=''
    solution.save()
    #cache.clear()
    #print(solution.solution_id)
    payload=deque([])
    if cache.get(solution.user):
        payload=deque(cache.get(solution.user.username))
        payload.appendleft(solution)
        cache.set(solution.user,payload)
        
    else:
        payload.appendleft(solution)
        cache.set(solution.user,payload)

    #solutions=Solution.objects.filter(user=request.user).order_by('-solution_id')
    return render(request,'leaderboard.html',{'solutions':payload})

    #return render(request,render_file,context)



def leaderboard(request):
    solutions=Solution.objects.all()
    print(solutions)
    return render(request,'leaderboard.html',{'solutions':solutions})


