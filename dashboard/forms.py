from django import forms
from django.contrib.auth.models import User
from dashboard.models import Homework, Note, Task
from django.contrib.auth.forms import UserCreationForm


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'notetitle',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'notedesc',
                }
            )
        }


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'deadline', 'completed']
        widgets = {
            'subject': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'subject',
                    'required': 'true',
                }
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'title',
                    'required': 'true',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'id': 'desc',
                }
            ),
            'deadline': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'id': 'deadline',
                    'required': 'true',
                }
            ),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'completed']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'title',
                    'required': 'true',
                }
            ),
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']