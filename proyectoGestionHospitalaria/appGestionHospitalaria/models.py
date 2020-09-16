from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    """
    Modelo que representa un Medico
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Siempre asociado a usuario
    matricula = models.CharField(max_length=100)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.user.get_full_name(), self.matricula)

class Patient(models.Model):
    """
    Modelo que representa un paciente
    """
    first_name = models.CharField(max_length=100) #Puede no tener asociado un usuario
    last_name = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True, help_text="Ingrese Numero de documento")
    date_of_birth = models.DateField(null=True, blank=True)
    obra_Social = models.CharField(max_length=100)
    phone_number  = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('patient-detail', args=[str(self.id)])

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']

class Estudio(models.Model):
    """
    Modelo que representa un Estudio clinico
    """
    name = models.CharField(max_length=100)
    time_long = models.IntegerField()
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE , null=False) #siempre se asocia a un paciente
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, help_text="Ingrese una descripcion del estudio")

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.name, self.patient.__str__())