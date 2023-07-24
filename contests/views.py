from django.shortcuts import render,redirect
from django.dispatch import receiver
from django.http import HttpResponse,JsonResponse,HttpRequest
from .models import Contest,Question,Testcases,Submission,Score
from django.utils import timezone
from pathlib import Path
from datetime import timedelta
from .tasks import start_contest, end_contest
import os,filecmp,subprocess
import time
from django.core.cache import cache
from datetime import datetime
from django.utils import timezone
import threading
import time
from django.contrib.auth.decorators import login_required
# Create your views here.
from .tasks import process_submission
BASE_DIR = Path(__file__).resolve().parent.parent

def timeout_handler():
    flag=-2
    raise TimeoutError

@login_required
def contestshome(request):    
    if cache.get('allcontests'):
        contests=cache.get('allcontests')
    else:
        contests=Contest.objects.all()
        cache.set('allcontests',contests,timeout=24*60)
    #contest_id = 1
    #start_datetime = datetime(2023, 7, 7, 17, 5, 0)  # Replace with your desired start date and time
    #end_datetime = datetime(2023, 7, 7, 17, 8, 0)  # Replace with your desired end date and time

    # Schedule contest start and end tasks
    
    #return HttpResponse('Contest ended')
    return render(request,'contestshome.html',{'contests':contests})

def get_contest_status(request,contest_id):
    contest=Contest.objects.get(pk=contest_id)    
    rem_time=(contest.start_time-timezone.now()).total_seconds()    
    contest_end_time=contest.end_time.isoformat()

    return JsonResponse({'status':contest.is_active,'contest_end_time':contest_end_time,'rem_time':rem_time})
@login_required
def contest_detail(request,contest_id):
    contest_detail_contest={}
    contest_detail_question={}

    if cache.get('contest_detail_contest'):
        contest_detail_contest=cache.get('contest_detail_contest')
        if contest_id in contest_detail_contest:
            contest=contest_detail_contest
        else:
            contest=Contest.objects.get(pk=contest_id)
            contest_detail_contest[contest_id]=contest
            cache.set('contest_detail_contest',contest_detail_contest,timeout=24*60)
    else:
        contest=Contest.objects.get(pk=contest_id)
        contest_detail_contest[contest_id]=contest
        cache.set('contest_detail_contest',contest_detail_contest,timeout=24*60)
    if cache.get('contest_detail_question'):
        contest_detail_question=cache.get('contest_detail_question')
        if contest_id in contest_detail_question:
            questions=contest_detail_question[contest_id]
        else:
            questions=Question.objects.filter(contest=contest)
            contest_detail_question[contest_id]=questions
            cache.set('contest_detail_question',contest_detail_question,timeout=24*60)
            
    else:
        questions=Question.objects.filter(contest=contest)
        contest_detail_question[contest_id]=questions
        cache.set('contest_detail_question',contest_detail_question,timeout=24*60)
        
    #if contest.is_active:    
        #questions=[]           
        #questions=Question.objects.filter(contest=contest)        
    return render(request,'contestdetail.html',{'questions':questions,'contest_id':contest_id})
    #else:
        #if contest.end_time<=timezone.now():return HttpResponse("Contest will start soon!!!")
        #else:return HttpResponse("Contest ended!!!")



    
@login_required
def questionDetail(request,contest_id,question_id):
    if cache.get(str(question_id)):
        question,testcases=cache.get(str(question_id))
    else:
        question=Question.objects.get(pk=question_id)
        testcases=Testcases.objects.filter(question=question,is_sample_testcase=True)
        cache.set(str(question_id),(question,testcases),timeout=24*60)
    
    
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
@login_required
def submitQuestion(request,contest_id,question_id):
    submit_question={}
    f=request.FILES['solution']    
    with open(str(BASE_DIR) + '/static/solution.py','wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    if cache.get('submit_question'):
        submit_question=cache.get('submit_question')
        if (contest_id,question_id) in submit_question:
            contest,question=submit_question[(contest_id,question_id)]
        else:
            question=Question.objects.get(pk=question_id)
            contest=Contest.objects.get(pk=contest_id)
            submit_question[(contest_id,question_id)]=(contest,question)
            cache.set('submit_question',submit_question,timeout=24*60)
        
    else:
        question=Question.objects.get(pk=question_id)
        contest=Contest.objects.get(pk=contest_id)
        submit_question[(contest_id,question_id)]=(contest,question)
        cache.set('submit_question',submit_question,timeout=24*60)        
        
    python_file_path = str(BASE_DIR) + '/static/solution.py'
    process_submission_result = process_submission.delay(question_id,python_file_path) 
    verdict = process_submission_result.get()   
    if contest.is_active=="active":
        if verdict=="Accepted":
            exists = Submission.objects.filter(user=request.user,question=question,verdict=verdict)
            print(exists)
            if not exists:    
                score, created = Score.objects.get_or_create(contest=contest,user=request.user)           
                if created:print("created")
                score.total_points+=question.points
                score.last_accepted=timezone.now()+timedelta(minutes=score.penalties*600)
                score.save()
        else:
            score, created = Score.objects.get_or_create(contest=contest,user=request.user)
            score.penalties+=1
            score.save()


        #if verdict==1:
            #score.total_points+=question.points*(1-score.penalties*0.25)        
            #score.last_accepted=timezone.now()
        #else:
            #score.penalties+=1
            #print(score.penalties)
        #score.save()
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
@login_required 
def submissions(request,contest_id,question_id):
        if cache.get('q'+str(question_id)):
            question=cache.get('q'+str(question_id))            
        else:    
            question=Question.objects.get(pk=question_id)      
            cache.set('q'+str(question_id),question,timeout=24*60)

        solutions=Submission.objects.filter(user=request.user,question=question).order_by('-id')
        return render(request,'submissions.html',{'solutions':solutions,'iscontest':True})
                    

    
    #print(cache.exists('cached_submissions'))
    #solutions=Solution.objects.filter(user=request.user,problem=problem).order_by('-solution_id')
    #print(solutions)
        
@login_required
def allsubmissions(request,contest_id,question_id):
    if cache.get('q'+str(question_id)):
        question=cache.get('q'+str(question_id))            
    else:    
        question=Question.objects.get(pk=question_id)      
        cache.set('q'+str(question_id),question,timeout=24*60)
    
    solutions=Submission.objects.filter(question=question).order_by('-id')        
    return render(request,'submissions.html',{'solutions':solutions,'iscontest':True})
@login_required
def editorial(request,contest_id,question_id):
    if cache.get('q'+str(question_id)):
        question=cache.get('q'+str(question_id))          
    else:    
        question=Question.objects.get(pk=question_id)    
        cache.set('q'+str(question_id),question,timeout=24*60)
    #problem=get_object_or_404(Problem,pk=problem_id)    
    return render(request,'editorial.html')

@login_required
def leaderboard(request,contest_id): 
    leaderboard_contest={}
    if cache.get('leaderboard_contest'):
        leaderboard_contest=cache.get('leaderboard_contest')
        if contest_id in leaderboard_contest:
            contest=leaderboard_contest[contest_id]
        else:
            contest=Contest.objects.get(pk=contest_id)
            leaderboard_contest[contest_id]=contest
            cache.set('leaderboard_contest',leaderboard_contest,timeout=24*60)
    else:
        contest=Contest.objects.get(pk=contest_id)
        leaderboard_contest[contest_id]=contest
        cache.set('leaderboard_contest',leaderboard_contest,timeout=24*60)
    payload=[]    
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
