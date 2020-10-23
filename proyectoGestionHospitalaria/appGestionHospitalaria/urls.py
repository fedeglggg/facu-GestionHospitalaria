from django.urls import path
from django.urls import include
from django.conf.urls import url
from . import views



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
    path('turnos/crear/1', views.create_turno_1, name='create_turno_1'),
    path('turnos/crear/2/', views.create_turno_2, name='create_turno_2'),
    path('turnos/crear/2/3/', views.create_turno_3, name='create_turno_3')
]




