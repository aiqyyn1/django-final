import form as form
from django import forms
from .models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['tittle', 'description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'tittle', 'description', 'due', 'is_finished']
class DashboardForm(forms.Form):
    text = forms.CharField(max_length=255,label='Enter Your Search :')

