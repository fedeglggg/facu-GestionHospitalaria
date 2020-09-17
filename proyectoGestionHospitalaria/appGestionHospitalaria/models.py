from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Medico(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.IntegerField()

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    obra_social = models.CharField(max_length=1)
