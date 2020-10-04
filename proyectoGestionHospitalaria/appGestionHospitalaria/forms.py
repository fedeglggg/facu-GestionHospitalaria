from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db import models
from .models import Especialidad, Doctor


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    matricula = forms.CharField(max_length=100, required=False)
    especialidad = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'matricula', 'especialidad', 'password1', 'password2')

class MedicoProfileForm(ModelForm):
    class Meta:
        model = Doctor
        fields = {'user','matricula','especialidad'}