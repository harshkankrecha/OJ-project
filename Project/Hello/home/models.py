from enum import unique
from tkinter import CASCADE
from xml.parsers.expat import model
from django.db import models

from django.contrib.auth.models import User

class Questions(models.Model):
    question_id=models.IntegerField()
    question_name=models.CharField(max_length=255)
    description=models.TextField(blank=True)

    

    def __str__(self):
        return self.question_name
    
class Userclass(models.Model):
    userid=models.IntegerField()
    user_name=models.CharField(max_length=255)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name




    


