from django.contrib import admin
from django.urls import path,include
from . import views


app_name = 'contests'
urlpatterns = [    
    path('', views.contestshome,name='contestshome'), 
    path('contest/<int:contest_id>/get_contest_status/', views.get_contest_status,name='get_contest_status'),   
    path('contest/<int:contest_id>/', views.contest_detail,name='contest_detail'),    
    path('contest/<int:contest_id>/leaderboard', views.leaderboard,name='leaderboard'),
    path('contest/<int:contest_id>/problem/<int:question_id>/', views.questionDetail,name='question_detail'),
    path('contest/<int:contest_id>/problem/<int:question_id>/submit/', views.submitQuestion,name='submit_question'),
    path('contest/<int:contest_id>/problem/<int:question_id>/submissions/', views.submissions,name='submissions'),
    path('contest/<int:contest_id>/problem/<int:question_id>/allsubmissions/', views.allsubmissions,name='allsubmissions'),
    path('contest/<int:contest_id>/problem/<int:question_id>/editorial/', views.editorial,name='editorial'),


]   
admin.site.site_header = "Codemaster Admin"
admin.site.index_title = "Welcome to Codemaster"
admin.site.site_title = "Codemaster"