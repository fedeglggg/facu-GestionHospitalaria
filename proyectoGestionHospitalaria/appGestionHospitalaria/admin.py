from django.contrib import admin
from .models import patient, doctor, estudio, especialidad, obra_social

# Register your models here.

admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(estudio)
admin.site.register(especialidad)
admin.site.register(obra_social)

