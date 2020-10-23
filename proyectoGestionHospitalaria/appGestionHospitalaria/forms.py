from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime
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

# los fields se usan en el is_valid() matcheandolos con los names de los input 
# no se usa los id_nombredefield ej id_username para algo, no recuerdo -> chequear esto dsp

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

# para que pase el .is_valid()
class CreateFormTurno(ModelForm):
    tipo_estudio_name = forms.CharField(max_length=30)
    doctor_name = forms.CharField(max_length=30)
    paciente_name = forms.CharField(max_length=30)
    date = forms.DateField(required=True)
    #timeFrom = forms.ChoiceField(choices=horarios, required=True, label="Seleccione su horario")
    timeFrom = forms.TimeField(required=True)
    #timeTo = forms.TimeField(required=True)

    class Meta:
        model = Turno
        fields = ('tipo_estudio_name', 'doctor_name', 'date', 'timeFrom')

# si usas ModelForm chequea que sea el unico existente en la bd con el is_valid() en la view
class EspecialidadForm(forms.Form):
    name = forms.CharField(max_length=100, help_text="Ingrese el nombre de la especialidad (p. ej. Neurología, Traumatología etc.)")
    class Meta:
        model = Especialidad
        fields = ('name',)

class CreateFormTurno33(ModelForm):
    tipo_estudio_name = forms.CharField(max_length=30)
    doctor_name = forms.CharField(max_length=30)
    date = forms.DateField(required=True)
    timeFrom = forms.TimeField(required=True)
    #timeTo = forms.TimeField(required=True)

    class Meta:
        model = Turno
        fields = ('tipo_estudio_name', 'doctor_name', 'date', 'timeFrom')


