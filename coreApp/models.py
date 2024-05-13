from django.db import models

# Create your models here.
class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=64, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Course'


class Department(models.Model):
    dept_name = models.CharField(primary_key=True, max_length=32)
    building = models.CharField(max_length=32, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    

    class Meta:
        managed = False
        db_table = 'Department'

    def __str__(self):
       return f'{self.dept_name}'


class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Instructor'


class Prereq(models.Model):
    course = models.OneToOneField(Course, models.DO_NOTHING, primary_key=True)  # The composite primary key (course_id, preq_id) found, that is not supported. The first column is selected.
    preq = models.ForeignKey(Course, models.DO_NOTHING, related_name='prereq_preq_set')

    class Meta:
        managed = False
        db_table = 'Prereq'
        unique_together = (('course', 'preq'),)


class Section(models.Model):
    course = models.OneToOneField(Course, models.DO_NOTHING, primary_key=True)  # The composite primary key (course_id, sec_id, semester, year) found, that is not supported. The first column is selected.
    sec_id = models.CharField(max_length=4,unique=True)
    semester = models.IntegerField(unique=True)
    year = models.IntegerField(unique=True)
    building = models.CharField(max_length=32, blank=True, null=True)
    room = models.CharField(max_length=8, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Section'
        unique_together = (('course', 'sec_id', 'semester', 'year'),)


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Student'


class Takes(models.Model):
    student = models.OneToOneField(Student, models.DO_NOTHING, primary_key=True)  # The composite primary key (student_id, course_id, sec_id, semester, year) found, that is not supported. The first column is selected.
    course = models.ForeignKey(Section, models.DO_NOTHING)
    sec = models.ForeignKey(Section, models.DO_NOTHING, to_field='sec_id', related_name='takes_sec_set')
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', to_field='semester', related_name='takes_semester_set')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', to_field='year', related_name='takes_year_set')
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Takes'
        unique_together = (('student', 'course', 'sec', 'semester', 'year'),)


class Teaches(models.Model):
    course = models.OneToOneField(Section, models.DO_NOTHING, primary_key=True)  # The composite primary key (course_id, sec_id, semester, year, teacher_id) found, that is not supported. The first column is selected.
    sec = models.ForeignKey(Section, models.DO_NOTHING, to_field='sec_id', related_name='teaches_sec_set')
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', to_field='semester', related_name='teaches_semester_set')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', to_field='year', related_name='teaches_year_set')
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Teaches'
        unique_together = (('course', 'sec', 'semester', 'year', 'teacher'),)

class Publication(models.Model):
    p = models.OneToOneField(Instructor, models.DO_NOTHING, primary_key=True)  # The composite primary key (p_id, title) found, that is not supported. The first column is selected.
    title = models.CharField(max_length=50)
    journal = models.CharField(max_length=50, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    start_page = models.IntegerField(blank=True, null=True)
    end_page = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Publication'
        unique_together = (('p', 'title'),)

class ProfessorFunding(models.Model):
    p = models.OneToOneField(Instructor, models.DO_NOTHING, primary_key=True)  # The composite primary key (p_id, title) found, that is not supported. The first column is selected.
    title = models.CharField(max_length=50)
    funding = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Professor_Funding'
        unique_together = (('p', 'title'),)