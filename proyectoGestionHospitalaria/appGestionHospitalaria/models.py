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
    # especialidad = models.ManyToManyField(Especialidad, help_text="Seleccione una especialidad")
    especialidad = models.ManyToManyField(Especialidad)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """

        return self.user.get_full_name()
        #return '%s (%s)' % (self.user.get_full_name(), self.matricula)

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
        # return '{} {} {}'.format(self.user.get_full_name())
        return self.user.get_full_name()

class TipoEstudio(models.Model):
    """
    Modelo que representa un Tipo de estudio
    """
    name = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad,on_delete=models.CASCADE, help_text="Seleccione una especialidad", null=True, blank=True)
    # duration = models.IntegerField()

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        return self.name


class Estudio(models.Model):
    """
    Modelo que representa un Estudio clinico
    """
    tipo = models.ForeignKey(TipoEstudio, on_delete=models.CASCADE, null=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE , null=False) # siempre se asocia a un paciente
    comments = models.TextField(null=True, blank=True, help_text="Ingrese comentarios (Será visible para el paciente)", default="")
    diagnostic = models.TextField(null=True, blank=True, help_text="Ingrese un diagnóstico (No será visible para el paciente)", default="")
    confirmed = models.BooleanField(default=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False, blank=True)  # siempre se asocia a doctor
    secretary = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  #opcional

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        # return '%s (%s)' % (self.type.__str__(), self.paciente.__str__())
        return 'Tipo: ' + self.tipo.name + ' - Paciente: ' + self.paciente.__str__()+' - Médico: '+self.doctor.__str__()


class EstudioFile(models.Model):
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE, null=False)
    file = models.FileField(upload_to ='uploads/')
    descripcion = models.CharField(max_length=20, null=False, help_text="Ingrese descriptivo del archivo")

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """

        # return '%s (%s)' % (self.type.__str__(), self.paciente.__str__())
        return self.descripcion

class Turno(models.Model):
    """
    Modelo que representa un Turno
    """
    estudio = models.OneToOneField(Estudio, on_delete=models.CASCADE , null=False, primary_key=True)
    date = models.DateField(null=False)
    timeFrom = models.TimeField(null=False)
    #timeTo = models.TimeField(null=True, blank=True)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        #return '%s %s(%s-%s)' % (self.estudio.__str__(), self.date , self.timeFrom, self.timeTo)
        return 'fecha: ' + str(self.date) + ' - horario:' + str(self.timeFrom)

class DiaJornada(models.Model):
    nombre = models.CharField(max_length=9)
    def __str__(self):
        return self.nombre

class TurnoJornada(models.Model):
    dia = models.ForeignKey(DiaJornada, on_delete=models.CASCADE, null=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=False)
    horario_inicio = models.TimeField(null=False)
    horario_fin = models.TimeField(null=False)

    def __str__(self):
        return  self.doctor.user.first_name + ' ' + self.doctor.user.last_name + ' | ' + self.dia.nombre + ' | ' + str(self.horario_inicio) + ' - ' + str(self.horario_fin)