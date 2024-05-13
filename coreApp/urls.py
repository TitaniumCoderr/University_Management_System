# coreApp/urls.py

from django.urls import path
from . import views

app_name = 'coreApp'  # Specify the app namespace

urlpatterns = [
    path('roster/', views.prof_stats, name='prof_stats'),  # Assign a name to the URL pattern
    path('namesort/', views.sort_prof_name, name='sort_prof_name'),  # Assign a name to the URL pattern
    path('deptsort/', views.sort_prof_dept, name='sort_prof_dept'),
    path('salarysort/', views.sort_prof_salary, name='sort_prof_salary'),
    path('salary_stats/', views.salary_statistics_by_department, name='salary_statistics_by_department'),
    path('performance/', views.performance, name='performance'),
    path('professor_sections/', views.professor_sections, name='professor_sections'),
    path('student_list/', views.student_list, name='student_list'),
    path('course_section/', views.course_section, name='course_section'),
    
   
]
