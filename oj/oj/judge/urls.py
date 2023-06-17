from django.contrib import admin
from django.urls import path,include
from . import views

app_name = 'judge'
urlpatterns = [
    path('problems/', views.problems,name='problems'),
    path('', views.home,name='home'),
    path('problem/<int:problem_id>/', views.problemDetail,name='problem_detail'),
    path('problem/<int:problem_id>/submit/', views.submitProblem,name='submit'),
    path('leaderboard/', views.leaderboard,name='leaderboard'),
]
admin.site.site_header = "Codehelp Admin"
admin.site.index_title = "Welcome to Codehelp"
admin.site.site_title = "Codehelp"
    