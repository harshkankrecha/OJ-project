from django.db import models
from datetime import date
import django.utils
from django import forms

# Create your models here.
class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    current_weight=models.IntegerField(default=0)
    goal_weight=models.IntegerField(default=0)
    email=models.EmailField(max_length=255,default='')
    age=models.IntegerField(default=0)
    bmi=models.IntegerField(default=0)
    gender=models.CharField(max_length=10)
    address=models.TextField()
    date=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.first_name+' '+self.last_name
    
class Queries(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    mobile_number=models.IntegerField(('mobile_number'),default=0000000000,
   blank=True)
    user_message=models.TextField()

    def __str__(self):
        return self.first_name+' '+self.last_name

