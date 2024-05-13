from django.shortcuts import render
from django.http import HttpResponse
from .models import Student, Instructor,Teaches,Section,ProfessorFunding,Publication
from django.db.models import Avg,Min,Max,F,Count
from django.db import connection
from .forms import Form,StudentListForm,DepartmentForm
from datetime import date

#===============navigation=======================
def landing(request):
    return render(request, 'landing.html')

def admin(request):
    return render(request, 'admin.html')

def instructor(request):
    return render(request, 'instructor.html')

def student(request):
    return render(request, 'student.html')

#====================================PROFESSOR FUNCTIONALITIES===================================================
#============================INSTRUCTOR STATS (ADMIN)=========================
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
def prof_stats(request):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM Instructor;"
        cursor.execute(query)
        prof = dictfetchall(cursor)
    finally:
        cursor.close()

    context = {
        'prof': prof
    }
    return render(request, 'roster.html', context)


def sort_prof_name(request):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM Instructor order by name;"
        cursor.execute(query)
        prof = dictfetchall(cursor)
    finally:
        cursor.close()

    context = {
        'prof': prof
    }
    return render(request, 'roster.html', context)

def sort_prof_dept(request):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM Instructor order by dept_name;"
        cursor.execute(query)
        prof = dictfetchall(cursor)
    finally:
        cursor.close()

    context = {
        'prof': prof
    }
    return render(request, 'roster.html', context)

def sort_prof_salary(request):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM Instructor order by salary;"
        cursor.execute(query)
        prof = dictfetchall(cursor)
    finally:
        cursor.close()

    context = {
        'prof': prof
    }
    return render(request, 'roster.html', context)

#=================SALARY STATS (ADMIN)================================
def salary_statistics_by_department(request):
    salary_stats_by_dept = Instructor.objects.values('dept_name').annotate(
        min_salary=Min('salary'),
        max_salary=Max('salary'),
        avg_salary=Avg('salary')
    ).order_by('dept_name')
    
    return render(request, 'salary_stats.html', {'salary_stats_by_dept': salary_stats_by_dept})

#================================PERFORMANCE (ADMIN)==============================================
from datetime import date

def performance(request):

    start_date = None  # Default value for start_date
    end_date = None  # Default value for end_date

    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            year = form.cleaned_data["year"]
            semester = form.cleaned_data["semester"]

            if semester == '2':
                start_date = date(year, 1, 1)
                end_date = date(year, 5, 31)
            elif semester == '1':
                start_date = date(year, 8, 1)
                end_date = date(year, 12, 31)

            cursor = connection.cursor()
            try:
                instructor = Instructor.objects.get(name=name)

                # Query to count the number of course sections taught by the instructor
                num_sections_taught = '''
                    SELECT COUNT(*)
                    FROM Section
                    WHERE EXISTS (
                        SELECT course_id
                        FROM Teaches
                        WHERE teacher_id = %s
                        AND Teaches.course_id = Section.course_id
                    )
                    AND semester = %s
                    AND year = %s;
                '''
                with connection.cursor() as cursor:
                    cursor.execute(num_sections_taught, [instructor.id, semester, year])
                    row_section = dictfetchall(cursor)[0]['COUNT(*)']  # Fetch one row

                # Query to calculate the sum of capacities for sections taught by the instructor
                query_capacity = '''
                    SELECT SUM(capacity)
                    FROM Section
                    WHERE EXISTS (
                        SELECT course_id
                        FROM Teaches
                        WHERE teacher_id = %s
                        AND Teaches.course_id = Section.course_id
                    )
                    AND semester = %s
                    AND year = %s;
                '''
                with connection.cursor() as cursor:
                    cursor.execute(query_capacity, [instructor.id, semester, year])
                    row_capacity = cursor.fetchone()  # Fetch one row
                    # Extract capacity value from row_capacity (convert Decimal to int)
                    row_capacity_value = int(row_capacity[0]) if row_capacity and row_capacity[0] is not None else None

                # Query to funding the professor has secured
                query_funding = '''
                    SELECT SUM(funding)
                    FROM Professor_Funding
                    WHERE p_id = %s
                    AND start_date <= %s 
                    AND end_date >= %s;
                '''
                with connection.cursor() as cursor:
                    cursor.execute(query_funding, [instructor.id, end_date, start_date])
                    funding = cursor.fetchone()[0]  # Fetch one row

                # Query number of papers the professor has published
                query_publishing = '''
                    SELECT COUNT(title)
                    FROM Publication
                    WHERE p_id = %s
                    AND date <= %s 
                    AND date >= %s;
                '''
                with connection.cursor() as cursor:
                    cursor.execute(query_publishing, [instructor.id,end_date, start_date])
                    publishing = cursor.fetchone()[0]  # Fetch one row

                # Prepare context data to pass to the template
                context = {
                    'form': form,
                    'id': instructor.id,
                    'name': name,
                    'year': year,
                    'semester': semester,
                    'funding': funding,
                    'publishing': publishing,
                    'row_section': row_section,
                    'row_capacity': row_capacity_value,  # Convert Decimal object to int
                }

                return render(request, 'performance.html', context)

            except Instructor.DoesNotExist:
                return render(request, 'performance.html', {"result": -1, "form": form})
                # Handle the case when the instructor does not exist

    else:
        form = Form()

    # Render the form without results initially
    return render(request, 'performance.html', {'form': form})

#====================================PROFESSOR FUNCTIONALITIES===================================================
def professor_sections(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            year = form.cleaned_data["year"]
            semester = form.cleaned_data["semester"]
            
            cursor = connection.cursor()
            try:
                instructor = Instructor.objects.get(name=name)
                query = '''
                   SELECT *
                   FROM Section
                   WHERE EXISTS (
                       SELECT course_id
                       FROM Teaches
                       WHERE teacher_id = %s
                       AND Teaches.course_id = Section.course_id
                   )
                   AND semester = %s
                   AND year = %s;'''
                with connection.cursor() as cursor:
                    cursor.execute(query, [instructor.id, semester, year])
                    sec_result = dictfetchall(cursor)

                    context={
                        'form':form,
                        'sec_result':sec_result
                    }
                    return render(request, 'professor_sections.html', context)

            except Instructor.DoesNotExist:
                print("None found")
                
    else:
        form = Form()

    return render(request, 'professor_sections.html', {'form': form})

def student_list(request):
    if request.method == 'POST':
        form = StudentListForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            course= form.cleaned_data["course"]
            section = form.cleaned_data["section"]
            semester = form.cleaned_data["semester"]
            year = form.cleaned_data["year"]
            
            cursor = connection.cursor()
            try:
                instructor = Instructor.objects.get(name=name)
                query = '''
    SELECT Student.name, T1.student_id, Student.dept_name, Student.total_credits
    FROM Student
    JOIN (
        SELECT student_id
        FROM Takes
        WHERE course_id IN (
            SELECT course_id FROM Teaches WHERE teacher_id=%s)
        AND course_id = %s
        AND semester = %s
        AND sec_id = %s
        AND year = %s
    ) AS T1 ON Student.student_id = T1.student_id;
'''

                with connection.cursor() as cursor:
                    cursor.execute(query, [instructor.id,course, semester,section,year])
                    sec_result = dictfetchall(cursor)

                    context={
                        'form':form,
                        'name':name,
                        'section':section,
                        'semester':semester,
                        'course':course,
                        'year':year,
                        'sec_result':sec_result
                    }
                    return render(request, 'student_list.html', context)

            except Instructor.DoesNotExist:
                print("None found")
                
    else:
        form = StudentListForm()

    return render(request, 'student_list.html', {'form': form})

#=============================================Student=============================================
def course_section(request):
    if request.method == 'POST':
       form = DepartmentForm(request.POST)
       if form.is_valid():
           department = form.cleaned_data["department"]
           year = form.cleaned_data["year"]
           semester = form.cleaned_data["semester"]
           
           cursor = connection.cursor()
           try:
               
               query = '''
                      SELECT DISTINCT Section.course_id, T1.title
                        FROM Section
                        JOIN (
                            SELECT course_id, title
                            FROM Course
                            WHERE dept_name = %s
                        ) AS T1 ON Section.course_id = T1.course_id
                        WHERE Section.year = %s AND Section.semester = %s;
                   '''
               with connection.cursor() as cursor:
                   cursor.execute(query, [department,year, semester])
                   course_result = dictfetchall(cursor)
                   context={
                       'form':form,
                       'semester':semester,
                       'year':year,
                       'department':department,
                       'course_result':course_result
                   }
                   return render(request, 'course_section.html', context)
           except Instructor.DoesNotExist:
               print("None found")
               
    else:
        form = DepartmentForm()

    return render(request, 'course_section.html', {'form': form})