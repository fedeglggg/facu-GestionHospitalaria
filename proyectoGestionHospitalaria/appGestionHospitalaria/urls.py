from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('medicos/', views.medicos, name='lista_medicos'),
    path('medico/<int:doctor_id>/', views.medico, name='medico'),
    path('error/acceso/', views.error_acceso, name='error_acceso'),
    path('signup/paciente/', views.signup_paciente, name='signup_paciente'),
    path('signup/medico/', views.signup_medico, name='signup_medico'),
    path('pacientes/', views.pacientes, name='lista_pacientes'),
    path('paciente/<int:paciente_id>/', views.paciente, name='paciente'),
    path('turnos/', views.turnos, name='lista_turno'),
    path('historias/', views.historiasMedicas, name='lista_historia'),
    path('historia/<int:estudio_id>/', views.historia, name='historia'),
    path('turnos/crear/1/', views.create_turno_1, name='create_turno_1'),
    path('turnos/crear/2/', views.create_turno_2, name='create_turno_2'),
    path('turnos/crear/3/', views.create_turno_3, name='create_turno_3'),
    path('turnos/crear/4/', views.create_turno_4, name='create_turno_4')
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



