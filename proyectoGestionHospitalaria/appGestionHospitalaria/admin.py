from django.contrib import admin
from .models import Paciente, Doctor, Estudio, Especialidad, Obra_social, Turno, TipoEstudio, TurnoJornada, DiaJornada

# Register your models here.

admin.site.register(Paciente)
admin.site.register(Doctor)
admin.site.register(Estudio)
admin.site.register(Especialidad)
admin.site.register(Obra_social)
admin.site.register(Turno)
admin.site.register(TipoEstudio)

admin.site.register(TurnoJornada)
admin.site.register(DiaJornada)

