from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'judge'
urlpatterns = [
    path('problems/', views.problems,name='problems'),
    path('', views.home,name='home'),    
    path('problem/<int:problem_id>/', views.problemDetail,name='problem_detail'),
    path('problem/<int:problem_id>/submit/', views.submitProblem,name='submit'),
    path('problem/<int:problem_id>/submissions/', views.submissions,name='submissions'),
    path('problem/<int:problem_id>/allsubmissions/', views.allsubmissions,name='allsubmissions'),
    path('problem/<int:problem_id>/editorial/', views.editorial,name='editorial'),
    #path('problem/submit/', views.submitProblem,name='submit'),
    #path('submissions/', views.submissions,name='submissions'),
    #path('problem/<int:problem_id>/editorial', views.problemDetail,name='problem_detail'),
]
admin.site.site_header = "Codemaster Admin"
admin.site.index_title = "Welcome to Codemaster"
admin.site.site_title = "Codemaster"