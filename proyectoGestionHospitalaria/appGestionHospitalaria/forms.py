from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db import models
from .models import Especialidad, Doctor


class SignUpFormMedico(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    matricula = forms.CharField(max_length=32)
    especialidad = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'matricula', 'especialidad', 'password1', 'password2')

# los fields se usan en el is_valid() matcheandolos con los names de los input o los id_nombredefield ej id_username no recuerdo -> chequear esto dsp

class MedicoProfileForm(ModelForm):
    class Meta:
        model = Doctor
        fields = {'user','matricula','especialidad'}

class SignUpFormPaciente(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    dni = forms.IntegerField()
    date_of_birth = forms.DateField()
    obra_social = forms.CharField(max_length=32)
    phone_number  = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number' , 'dni', 'obra_social', 'date_of_birth', 'email', 'password1', 'password2')