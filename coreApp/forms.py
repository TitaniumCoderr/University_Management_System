from django import forms
from .models import Department


class Form(forms.Form):

    name =forms.CharField(label='Name', max_length=200, required=False,
                           widget= forms.TextInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Name',
                               'required': 'True'
                            }))
    year=forms.IntegerField(label="Year", required=False,
                           widget= forms.NumberInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Year',
                               'required': 'True'
                            }))
    semester = forms.IntegerField(label="Semster",required=False,
                           widget= forms.NumberInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Semester',
                               'required': 'True'
                            }))

class StudentListForm(forms.Form):

    name =forms.CharField(label='Name', max_length=200, required=False,
                           widget= forms.TextInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Name',
                               'required': 'True'
                            }))
    course = forms.CharField(label="Course",required=False,
                           widget= forms.TextInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Course',
                               'required': 'True'
                            }))
    section=forms.CharField(label="Section", required=False,
                           widget= forms.TextInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Section',
                               'required': 'True'
                            }))
    semester = forms.IntegerField(label="Semester",required=False,
                           widget= forms.NumberInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Semester',
                               'required': 'True'
                            }))
    year=forms.IntegerField(label="Year", required=False,
                           widget= forms.NumberInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Year',
                               'required': 'True'
                            }))
    

class DepartmentForm(forms.Form):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label=None
    )
    year=forms.IntegerField(label="Year", required=False,
                           widget= forms.NumberInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Year',
                               'required': 'True'
                            }))
    semester = forms.IntegerField(label="Semster",required=False,
                           widget= forms.NumberInput
                           (attrs={
                               'class': 'wiki-title',
                               'name': 'WikiTitle',
                               'placeholder':'Enter Semester',
                               'required': 'True'
                            }))

