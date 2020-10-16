from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class Obra_social(models.Model):
    name = models.CharField(max_length=100, help_text="Ingrese el nombre de la obra social")

    def __str__(self):
        return self.name


class Especialidad(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Ingrese el nombre de la especialidad (p. ej. Neurología, Traumatología etc.)")

    def __str__(self):
        return self.name

class Doctor(models.Model):
    """
    Modelo que representa un Medico
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 
    matricula = models.CharField(max_length=100)
    especialidad = models.ManyToManyField(Especialidad, help_text="Seleccione una especialidad")
 
    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.user.get_full_name(), self.matricula)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Doctor.objects.create(user=instance)
#     instance.doctor.save()


class Paciente(models.Model):
    """
    Modelo que representa un paciente
    """

    dni = models.IntegerField(unique=True, help_text="Ingrese Numero de documento")
    date_of_birth = models.DateField(null=True, blank=True)
    obra_social = models.ForeignKey(Obra_social, on_delete=models.SET_NULL, blank=True, null=True)
    phone_number  = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Talvez debería tener siempre asociado un usuario

    def get_absolute_url(self):
       pass

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        # solo si tiene que tener obligatoriamente un usuario, sino esto rompe todo
        return self.user.get_full_name()

class Estudio(models.Model):
    """
    Modelo que representa un Estudio clinico
    """
    name = models.CharField(max_length=100)
    time_long = models.IntegerField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE , null=False) # siempre se asocia a un paciente
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, help_text="Ingrese una descripcion del estudio")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)  # siempre se asocia a un paciente
    secretary = models.ForeignKey(User, on_delete=models.CASCADE, null=False)  # siempre se asocia a un paciente

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return '%s (%s)' % (self.name, self.paciente.__str__())



