from django.urls import path
from django.urls import include
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^Patients/$', views.patientsListView.as_view(), name='patients'),
    url(r'^Patient/(?P<pk>\d+)$', views.patientDetailView.as_view(), name='patient-detail'),
    #url(r'^patients/$', views.index, name='index'),
    #path('usuarios/', views.usuarios, name='usuarios'),
    #path('accounts/', include('django.contrib.auth.urls'))
]