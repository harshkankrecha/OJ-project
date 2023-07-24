from celery import shared_task
from .models import Problem,Solution,Testcases
from django.core.cache import cache
import subprocess
from pathlib import Path
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


@shared_task
def process_submission(problem_id,python_file_path):
    timeout = 5    
    verdict="Judging"
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
    #problem=Problem.objects.get(pk=problem_id)
    #test_data=Testcases.objects.filter(problem=problem)
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
