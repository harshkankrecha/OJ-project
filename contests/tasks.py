from celery import shared_task
from datetime import datetime
from .models import Contest,Testcases,Question
import time
from django.utils import timezone
from django.core.cache import cache
import subprocess
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent



def schedule_contest(contest_id):
    print(contest_id)
    contest=Contest.objects.get(pk=contest_id) 
    timepass_time=(contest.start_time-timezone.now()).total_seconds()
    timepass.delay(contest_id,timepass_time)




@shared_task
def timepass(contest_id,timepass_time):
    time.sleep(timepass_time)
    Contest.objects.filter(pk=contest_id).update(is_active='active')
    start_contest(contest_id)
    

def start_contest(contest_id):
    print(contest_id)
    contest=Contest.objects.get(pk=contest_id)  
    
    timepass_time=(contest.duration_minutes)*60
    print("Contest started!!!")
    print(contest.is_active)
    timepass_again.delay(contest_id,timepass_time)

@shared_task
def timepass_again(contest_id,timepass_time):
    time.sleep(timepass_time)
    contest=Contest.objects.get(pk=contest_id)
    print(contest.is_active)
    Contest.objects.filter(pk=contest_id).update(is_active='ended')
    print(contest.is_active)
    #contest.is_active=False
    #print(contest.is_active)
    end_contest(contest_id)    

def end_contest(contest_id):
    print(contest_id)  
    print("Contest ended!!!")

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



@shared_task
def process_submission(question_id,python_file_path):
    timeout = 5    
    verdict="Judging"
    cached_contest_testcases={}
    cached_questions_submit={}
    if cache.get('cached_questions_submit'):
        cached_questions_submit=cache.get('cached_questions_submit')
        if question_id in cached_questions_submit:
            question=cached_questions_submit[question_id]
            print("from the submit cache")
        else:
            question=Question.objects.get(pk=question_id)
            cached_questions_submit[question_id]=question
            cache.set('cached_questions_submit',cached_questions_submit,timeout=24*60)
    else:
        question=Question.objects.get(pk=question_id)
        cached_questions_submit[question_id]=question
        cache.set('cached_questions_submit',cached_questions_submit,timeout=24*60)
    #problem=Problem.objects.get(pk=problem_id)
    #test_data=Testcases.objects.filter(problem=problem)
    if cache.get('cached_contest_testcases'):
        cached_contest_testcases=cache.get('cached_contest_testcases')
        if question_id in cached_contest_testcases:
            test_data=cached_contest_testcases[question_id]
            print('taken from the cache')
        else:
            test_data = Testcases.objects.filter(question=question)
            cached_contest_testcases[question_id]=test_data
            cache.set('cached_contest_testcases',cached_contest_testcases,timeout=24*60)
    else:
        test_data = Testcases.objects.filter(question=question)
        cached_contest_testcases[question_id]=test_data
        cache.set('cached_contest_testcases',cached_contest_testcases)
    question=Question.objects.get(pk=question_id)
    test_data = Testcases.objects.filter(question=question)
    flag=count=1
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
    return verdict

    