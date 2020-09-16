from django.urls import path
from django.urls import include
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #path('', views.index, name='index'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('accounts/', include('django.contrib.auth.urls'))
]