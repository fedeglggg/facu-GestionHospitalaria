from django.urls import path
from django.urls import include
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Medicos/$', views.medicos, name='medicos'),
    url(r'^Medicos/registro/$', views.medicosSignin, name='registro de medicos'),
    url(r'^Patients/$', views.patientsListView.as_view(), name='patients'),
    url(r'^Patient/(?P<pk>\d+)$', views.patientDetailView.as_view(), name='patient-detail'),
    url(r'^Signup/$', views.signup, name='Signup'),
]

