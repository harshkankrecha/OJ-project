from django.shortcuts import render,get_object_or_404
from celery import shared_task
from .models import Problem,Testcases
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent.parent

    
    
        
    