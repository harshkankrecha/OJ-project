from django.shortcuts import render,redirect
from django.dispatch import receiver
from django.http import HttpResponse,JsonResponse,HttpRequest
from .models import Contest,Question,Testcases,Submission,Score
from django.utils import timezone
from pathlib import Path
from .signals import start_contest_signal,end_contest_signal
import os,filecmp,subprocess
import time
from django.core.cache import cache
import datetime
import threading
import time
# Create your views here.
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

def contestshome(request):
    contests=Contest.objects.all()
    return render(request,'contestshome.html',{'contests':contests})

def contest_detail(request,contest_id):
    contest=Contest.objects.get(pk=contest_id)
    if contest.is_active:    
        questions=[]               
        questions=Question.objects.filter(contest=contest)        
        return render(request,'contestdetail.html',{'questions':questions,'contest_id':contest_id})
    else:
        if contest.end_time<=timezone.now():return render(request,'contestend.html')
        else:return render(request,'beforecontest.html')
def contest_start(request):
    return redirect('/')

@receiver(start_contest_signal)
def contest_start_receiver(sender, instance, **kwargs):
    print("receiver called")
    return contest_start(None)
    

def questionDetail(request,contest_id,question_id):
    question=Question.objects.get(pk=question_id)
    testcases=Testcases.objects.filter(question=question,is_sample_testcase=True)
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
    return render(request,'questiondetail.html',{'question':question,'sample_testcase_data':sample_testcase_data})

def submitQuestion(request,contest_id,question_id):
    f=request.FILES['solution']    
    with open(str(BASE_DIR) + '/static/solution.py','wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    question=Question.objects.get(pk=question_id)
    flag=count=1
    python_file_path = str(BASE_DIR) + '/static/solution.py'
    test_data = Testcases.objects.filter(question=question)
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
    contest=Contest.objects.get(pk=contest_id) 
    score, created = Score.objects.get_or_create(contest=contest,user=request.user)           
    if created:print("created")

    if flag==1:
        score.total_points+=question.points*(1-score.penalties*0.25)
        
        score.last_accepted=timezone.now()
    else:
        score.penalties+=1
        print(score.penalties)
    score.save()
    submission=Submission()
    submission.user=request.user
    submission.question=question
    submission.verdict=verdict
    if verdict=="Accepted":
        question.users.add(request.user)   
   
    
    #problem.verdict=verdict
    submission.submitted_at=timezone.now()
    submission.submitted_code=python_file_path    
    #solution.submitted_code=''
    submission.save()
    
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
    
def submissions(request,contest_id,question_id):  
    
        question=Question.objects.get(pk=question_id)           
        solutions=Submission.objects.filter(user=request.user,question=question).order_by('-id')
        return render(request,'submissions.html',{'solutions':solutions,'iscontest':True})
                    

    
    #print(cache.exists('cached_submissions'))
    #solutions=Solution.objects.filter(user=request.user,problem=problem).order_by('-solution_id')
    #print(solutions)
        

def allsubmissions(request,contest_id,question_id):
    question=Question.objects.get(pk=question_id)
    solutions=Submission.objects.filter(question=question).order_by('-id')        
    return render(request,'submissions.html',{'solutions':solutions,'iscontest':True})

def editorial(request,contest_id,question_id):
    #problem=get_object_or_404(Problem,pk=problem_id)    
    return HttpResponse("Comming Soon")


def leaderboard(request,contest_id): 
    payload=[]   
    contest=Contest.objects.get(pk=contest_id)
    if cache.get(f'leaderboard+{contest_id}'):
        payload=cache.get(f'leaderboard+{contest_id}')
        return render(request,'leaderboard.html',{'rankings':payload})
    else:
        payload=Score.objects.filter(contest=contest)
        payload=sorted(payload,key=lambda x:(-(x.total_points),x.last_accepted))
        
        rankings=[]
        count=1
        for obj in payload:
            rankings.append((count,obj))
            count+=1
        cache.set(f'leaderboard+{contest_id}',rankings,60)
        return render(request,'leaderboard.html',{'rankings':rankings})

        
    #return HttpResponse(f"Leaderboard for contest {contest_id}")




# Create and start the thread for scheduling the contest
#contest_id = 1  # Replace with the actual contest ID
#schedule_thread = threading.Thread(target=schedule_contest, args=(request,contest_id,))
#schedule_thread.start()
#schedule_thread.join()
