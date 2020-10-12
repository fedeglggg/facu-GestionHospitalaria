from django.urls import path
from django.urls import include
from django.conf.urls import url
from . import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('medicos/', views.medicos, name='medicos'),
    path('signup/paciente/', views.signup_paciente, name='signup_paciente'),
    path('signup/medico/', views.signup_medico, name='signup_medico'),
    path('pacientes/', views.pacientes, name='listado de pacientes'),
    path('paciente/<int:paciente_id>/', views.paciente, name='paciente')
]

