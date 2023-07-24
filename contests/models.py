from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
import time
from ckeditor.fields import RichTextField
from django.utils import timezone
from datetime import datetime,timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

class Contest(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField() 
    is_active=models.CharField(default='inactive',max_length=20)  

    def __str__(self):
        return self.name
    
class Score(models.Model):
    contest=models.ForeignKey(Contest, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    total_points=models.FloatField(default=0.0)
    penalties=models.IntegerField(default=0)
    last_accepted= models.DateTimeField(default=timezone.now()+timedelta(days=10))
    
                                     
    def __str__(self):
        return self.contest.name


    
class Question(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    problem_statement=RichTextField()
    code=models.CharField(max_length=255)
    users=models.ManyToManyField(User)
    input_statement=RichTextField()
    constraint_statement=RichTextField()
    output_statement=RichTextField()
    editorial=RichTextField(default="Coming Soon")
    points=models.IntegerField(default=0)

    def __str__(self):
        return self.name
 
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verdict=models.CharField(max_length=50)
    submitted_code=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.question.name}"
    
class Testcases(models.Model):
    input_file=models.FileField(upload_to='static/',default=None)
    answer_file=models.FileField(upload_to='static/',default=None)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    is_sample_testcase=models.BooleanField(default=False)

    def __str__(self):
        return self.question.name
