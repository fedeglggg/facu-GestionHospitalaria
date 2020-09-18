from django.urls import path
from django.urls import include
from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Medicos/$', views.medicos, name='medicos'),
    url('signup/', views.signup, name='signup'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^Medicos/registro/$', views.medicosSignup, name='registro de medicos'),
    url(r'^Pacientes/$', views.patientsListView.as_view(), name='pacientes'),
    url(r'^Paciente/(?P<pk>\d+)$', views.patientDetailView.as_view(), name='patient-detail')
]

