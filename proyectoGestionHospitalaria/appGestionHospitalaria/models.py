from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User




# Create your models here.

class Obra_social(models.Model):
    name = models.CharField(max_length=100, help_text="Ingrese el nombre de la especialidad (p. ej. Neurología, Traumatología etc.)")

    def __str__(self):
        return self.name


class Especialidad(models.Model):
    name = models.CharField(max_length=100, help_text="Ingrese el nombre de la especialidad (p. ej. Neurología, Traumatología etc.)")

    def __str__(self):
        return self.name

class Doctor(models.Model):
    """
    Modelo que representa un Medico
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Siempre asociado a usuario
    matricula = models.CharField(max_length=100)
    especialidad = models.ManyToManyField(Especialidad, help_text="Seleccione una especialidad")
    # ManyToManyField, porque un un doctor puede tener muchas especialidades, y una especialidad puede ser tenida por muchos doctores

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.user.get_full_name(), self.matricula)

class Paciente(models.Model):
    """
    Modelo que representa un paciente
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.IntegerField(unique=True, help_text="Ingrese Numero de documento")
    date_of_birth = models.DateField(null=True, blank=True)
    obra_social = models.ForeignKey(Obra_social, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number  = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)  # Puede o no tener un usuario asociado

    def get_absolute_url(self):
       pass

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
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE , null=False) # siempre se asocia a un paciente
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, help_text="Ingrese una descripcion del estudio")

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.name, self.paciente.__str__())



