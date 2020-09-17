from django.urls import path
from django.urls import include
from . import views
from .views import signup

urlpatterns = [
    path('', views.index, name='Inicio'),
    path('usuarios/', views.usuarios, name='Usuarios'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls'),
    )
]