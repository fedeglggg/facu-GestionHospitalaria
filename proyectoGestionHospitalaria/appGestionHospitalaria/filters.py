import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter

from .models import *

class DoctorFilter(django_filters.FilterSet):


    def __init__(self, *args, **kwargs):
        super(DoctorFilter, self).__init__(*args, **kwargs)
        self.filters['user__first_name'].label = "Nombre"
        self.filters['user__last_name'].label = "Apellido"
        self.filters['matricula'].label = "Matrícula"


    class Meta:
        model = Doctor
        fields = ['user__first_name', 'user__last_name', 'matricula']

class PatientFilter(django_filters.FilterSet):


    def __init__(self, *args, **kwargs):
        super(PatientFilter, self).__init__(*args, **kwargs)
        self.filters['user__first_name'].label = "Nombre"
        self.filters['user__last_name'].label = "Apellido"
        self.filters['dni'].label = "Dni"
        self.filters['obra_social'].label = "Obra Social"


    class Meta:
        model = Paciente
        fields = ['user__first_name', 'user__last_name', 'dni', 'obra_social', ]

