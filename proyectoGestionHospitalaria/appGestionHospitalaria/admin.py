from django.contrib import admin
from .models import *


# Register your models here.
class FileEstudioInLine(admin.TabularInline):
    model = EstudioFile
    extra = 0



admin.site.register(Paciente)
admin.site.register(Doctor)
@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'paciente', 'comments','diagnostic','confirmed','doctor','secretary')
    inlines = [FileEstudioInLine]

admin.site.register(Especialidad)
admin.site.register(Obra_social)
admin.site.register(Turno)

admin.site.register(TipoEstudio)

admin.site.register(TurnoJornada)
admin.site.register(DiaJornada)

