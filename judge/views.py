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
from collections import deque,defaultdict
import json
from django.http import JsonResponse
from .task import *
from django.views.decorators.csrf import csrf_exempt


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

cached_submissions=defaultdict(lambda:deque([]))

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
    #print(request.user.username)
    user=request.user
    user_data = {
        'username': user.username,        
    }
    user_json = json.dumps(user_data)
    context = {'user_json': user_json}
    return render(request,'home.html',context)

def problems(request):    
    cached_problems={}
    if cache.get('cached_problems'):
        cached_problems=cache.get('cached_problems')
        print("From the problems cache")
    else:
        problems_list=Problem.objects.all()
        for problem in problems_list:
            cached_problems[problem.pk]=problem
        cache.set('cached_problems',cached_problems,timeout=24*60)    
    context={'problems_list':cached_problems.values(),'user_obj':request.user}
    return render(request,'problems_list.html',context)


def problemDetail(request,problem_id):
    sample_testcases={}
    cached_problems_detail={}
    if cache.get('cached_problems_detail'):
        cached_problems_detail=cache.get('cached_problems_detail')
        if problem_id in cached_problems_detail:
            problem=cached_problems_detail[problem_id]
            print("from the details cache")
            #print("from the cache")
        else:
            problem=Problem.objects.get(pk=problem_id)
            cached_problems_detail[problem_id]=problem
            cache.set('cached_problems_detail',cached_problems_detail)
    else:
        problem=Problem.objects.get(pk=problem_id)
        cached_problems_detail[problem_id]=problem
        cache.set('cached_problems_detail',cached_problems_detail)
    
    
    if cache.get('sample_testcases'):
        #print(sample_testcases)
        sample_testcases=cache.get('sample_testcases')
        if problem_id in sample_testcases:
            testcases=sample_testcases[problem_id]
            print("from the cache")
        else:
            #print(sample_testcases)
            testcases=Testcases.objects.filter(problem=problem,is_sample_testcase=True)
            sample_testcases[problem_id]=testcases
            cache.set('sample_testcases',sample_testcases)
    else:
        #print(sample_testcases)
        testcases=Testcases.objects.filter(problem=problem,is_sample_testcase=True)
        sample_testcases[problem_id]=testcases
        cache.set('sample_testcases',sample_testcases)

    count=1
    sample_testcase_data=[]
    for testcase in testcases:
        input_file=testcase.input_file
        answer_file=testcase.answer_file
        input_file_path=str(BASE_DIR) + '/'+str(input_file)
        answer_file_path=str(BASE_DIR) + '/'+str(answer_file)
        with open(input_file_path, 'r') as file:
            input_file_data = file.read()
        with open(answer_file_path, 'r') as file:
            answer_file_data = file.read() 
        sample_testcase_data.append([input_file_data,answer_file_data,count])
        count+=1
    #print(sample_testcase_data)    
    #context={'problem':problem,'problem_id':problem_id}
    return render(request,'detail.html',{'problem':problem,'problem_id':problem_id,'sample_testcase_data':sample_testcase_data})
    
    #return render(request,'index.html',context)
    #return JsonResponse(context)
    #action="{% url 'judge:submit' problem.id %}"

def submitProblem(request,problem_id):    
    
    cached_testcases={}
    cached_problems_submit={}
    if cache.get('cached_problems_submit'):
        cached_problems_submit=cache.get('cached_problems_submit')
        if problem_id in cached_problems_submit:
            problem=cached_problems_submit[problem_id]
            print("from the submit cache")
        else:
            problem=Problem.objects.get(pk=problem_id)
            cached_problems_submit[problem_id]=problem
            cache.set('cached_problems_submit',cached_problems_submit,timeout=24*60)
    else:
        problem=Problem.objects.get(pk=problem_id)
        cached_problems_submit[problem_id]=problem
        cache.set('cached_problems_submit',cached_problems_submit,timeout=24*60)
        
    f=request.FILES['solution']    
    with open(str(BASE_DIR) + '/static/solution.py','wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    flag=count=1
    python_file_path = str(BASE_DIR) + '/static/solution.py'
    
    if cache.get('cached_testcases'):
        cached_testcases=cache.get('cached_testcases')
        if problem_id in cached_testcases:
            test_data=cached_testcases[problem_id]
            print('taken from the cache')
        else:
            test_data = Testcases.objects.filter(problem=problem)
            cached_testcases[problem_id]=test_data
            cache.set('cached_testcases',cached_testcases,timeout=24*60)
    else:
        test_data = Testcases.objects.filter(problem=problem)
        cached_testcases[problem_id]=test_data
        cache.set('cached_testcases',cached_testcases)

    timeout = 5    
    verdict="Judging"
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
            break
        if flag==-2:
            break
        # Store the output in a text file
        output_file_path = str(BASE_DIR) + '/static/output.txt'
        with open(output_file_path, 'w') as file:
            file.write(output)   

        if error:  
            flag=-1      
            print(error) 
            #error_type = (error.split('^')[1].strip()).split(':')[0]
            if "SyntaxError" in error:
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
    solution.problem=problem
    solution.verdict=verdict
    if verdict=="Accepted":
        problem.users.add(request.user)
    
    updated_cached_problems=cache.get('cached_problems_submit')
    updated_cached_problems[problem_id]=problem
    cache.set('cached_problems_submit',updated_cached_problems)
    #problem.verdict=verdict
    solution.submitted_at=timezone.now()
    solution.submitted_code=python_file_path    
    #solution.submitted_code=''
    solution.save()
    cache.delete('cached_allsubmissions')
    cache.delete('cached_submissions')
    """if cache.get('cached_submissions'):
        cached_submissions=cache.get('cached_submissions')
        cached_submissions[(request.user,problem_id)].appendleft(solution)
        cache.set('cached_submissions',cached_submissions)
    else:
        cached_submissions[(request.user,problem_id)].appendleft(solution)
        cache.set('cached_submissions',cached_submissions)"""


    #cache.clear()
    #print(solution.solution_id)
    """payload=deque([])
    if cache.get(solution.user):
        payload=deque(cache.get(solution.user.username))
        payload.appendleft(solution)
        cache.set(solution.user,payload)        
    else:
        payload.appendleft(solution)
        cache.set(solution.user,payload)"""

    #solutions=Solution.objects.filter(user=request.user).order_by('-solution_id')
    #return render(request,'leaderboard.html',{'solutions':solutions})
    #return JsonResponse({'verdict':verdict})
    #return render(request,render_file,context)
    #return render(request,'detail.html',{'problem':problem,'problem_id':problem_id,'verdict':verdict})
    #return HttpResponse(verdict)
    return JsonResponse({'verdict': verdict})
    #return redirect('/judge/submissions/')


def submissions(request,problem_id):  
    cached_submissions=defaultdict(list)
    cached_problems_submissions={}
    if cache.get('cached_problems_submissions'):
        cached_problems_submissions=cache.get('cached_problems_submissions')
        if problem_id in cached_problems_submissions:
            problem=cached_problems_submissions[problem_id]
            print("from the submissions cache")
            #print("from the cache")
        else:
            problem=Problem.objects.get(pk=problem_id)
            cached_problems_submissions[problem_id]=problem
            cache.set('cached_problems_submissions',cached_problems_submissions)
    else:
        problem=Problem.objects.get(pk=problem_id)
        cached_problems_submissions[problem_id]=problem
        cache.set('cached_problems_submissions',cached_problems_submissions)
    
    if cache.get('cached_submissions'):
        cached_submissions=cache.get('cached_submissions')
        if len(cached_submissions[(request.user,problem_id)])==0:
            payload=[]
            solutions=Solution.objects.filter(user=request.user,problem=problem).order_by('-solution_id')
            for solution in solutions:
                payload.append(solution)
            cached_submissions[(request.user,problem_id)]=payload
            cache.set('cached_submissions',cached_submissions)
        else:
            payload=cached_submissions[(request.user,problem_id)]
            print('submissions taken from the cache')
    else:
        payload=[]
        solutions=Solution.objects.filter(user=request.user,problem=problem).order_by('-solution_id')
        for solution in solutions:
            payload.append(solution)
        cached_submissions[(request.user,problem_id)]=payload
        cache.set('cached_submissions',cached_submissions)            

    
    #print(cache.exists('cached_submissions'))
    #solutions=Solution.objects.filter(user=request.user,problem=problem).order_by('-solution_id')
    #print(solutions)
    return render(request,'submissions.html',{'solutions':payload})

def allsubmissions(request,problem_id):
    #problem=get_object_or_404(Problem,pk=problem_id)
    cached_allsubmissions=defaultdict(list)
    cached_problems_allsubmissions={}
    if cache.get('cached_problems_allsubmissions'):
        cached_problems_allsubmissions=cache.get('cached_problems_allsubmissions')
        if problem_id in cached_problems_allsubmissions:
            problem=cached_problems_allsubmissions[problem_id]
            print("from the allsubmissions cache")
            #print("from the cache")
        else:
            problem=Problem.objects.get(pk=problem_id)
            cached_problems_allsubmissions[problem_id]=problem
            cache.set('cached_problems_allsubmissions',cached_problems_allsubmissions)
    else:
        problem=Problem.objects.get(pk=problem_id)
        cached_problems_allsubmissions[problem_id]=problem
        cache.set('cached_problems_allsubmissions',cached_problems_allsubmissions)
    
    if cache.get('cached_allsubmissions'):
        cached_allsubmissions=cache.get('cached_allsubmissions')
        if len(cached_allsubmissions[problem_id])==0:
            payload=[]
            solutions=solutions=Solution.objects.filter(problem=problem).order_by('-solution_id')
            for solution in solutions:
                payload.append(solution)
            cached_allsubmissions[problem_id]=payload
            cache.set('cached_allsubmissions',cached_allsubmissions)
        else:
            payload=cached_allsubmissions[problem_id]
            print('allsubmissions taken from the cache')
    else:
        payload=[]
        solutions=solutions=Solution.objects.filter(problem=problem).order_by('-solution_id')
        for solution in solutions:
            payload.append(solution)
        cached_allsubmissions[problem_id]=payload
        cache.set('cached_allsubmissions',cached_allsubmissions)     
    
    return render(request,'submissions.html',{'solutions':payload})

def editorial(request,problem_id):
    #problem=get_object_or_404(Problem,pk=problem_id)
    cached_problems_editorial={}
    if cache.get('cached_problems_editorial'):
        cached_problems_editorial=cache.get('cached_problems_editorial')
        if problem_id in cached_problems_editorial:
            problem=cached_problems_editorial[problem_id]
            print("from the editorial cache")
        else:
            problem=Problem.objects.get(pk=problem_id)
            cached_problems_editorial[problem_id]=problem
            cache.set('cached_problems_editorial',cached_problems_editorial)
    else:
        problem=Problem.objects.get(pk=problem_id)
        cached_problems_editorial[problem_id]=problem
        cache.set('cached_problems_editorial',cached_problems_editorial)
    
    editorial_text=problem.editorial
    return render(request,'editorial.html',{'editorial_text':editorial_text})

