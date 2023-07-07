from tkinter import CASCADE
from django.db import models
from pathlib import Path
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

class Problem(models.Model):
    name=models.CharField(max_length=255)
    problem_statement=RichTextField()
    code=models.CharField(max_length=255)
    users=models.ManyToManyField(User)
    input_statement=RichTextField()
    constraint_statement=RichTextField()
    output_statement=RichTextField()
    editorial=RichTextField(default="Coming Soon")

    def __str__(self):
        return self.name

class Solution(models.Model):
    solution_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    verdict=models.CharField(max_length=50)
    submitted_at=models.DateTimeField()
    submitted_code=models.CharField(max_length=255)    
    def __str__(self):
        return self.verdict

class Testcases(models.Model):
    input_file=models.FileField(upload_to=str(BASE_DIR)+'/static',default=None)
    answer_file=models.FileField(upload_to=str(BASE_DIR)+'/static',default=None)
    problem=models.ForeignKey(Problem,on_delete=models.CASCADE)
    is_sample_testcase=models.BooleanField(default=False)


    def __str__(self):
        return self.problem.name

