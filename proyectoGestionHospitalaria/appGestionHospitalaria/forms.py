from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db import models
from .models import Especialidad, Doctor, TipoEstudio, Turno


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

class CreateFormTurno(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=TipoEstudio.objects.all())
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    date = forms.DateField(required=True)
    timeFrom = forms.TimeField(required=True)
    #timeTo = forms.TimeField(required=True)

    class Meta:
        fields = ('name', 'doctor', 'date', 'timeFrom')

