import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, TimeFilter, IsoDateTimeFilter
from .models import *
from django import forms

class DoctorFilter(django_filters.FilterSet):
    matricula = NumberFilter("matricula", widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(DoctorFilter, self).__init__(*args, **kwargs)
        self.filters['user__first_name'].label = "Nombre "
        self.filters['user__last_name'].label = "Apellido "
        self.filters['matricula'].label = "Matrícula "


    class Meta:
        model = Doctor
        fields = ['user__first_name', 'user__last_name', 'matricula']

class PatientFilter(django_filters.FilterSet):
    dni = NumberFilter("dni", widget= forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(PatientFilter, self).__init__(*args, **kwargs)
        self.filters['user__first_name'].label = "Nombre "
        self.filters['user__last_name'].label = "Apellido "
        self.filters['dni'].label = "Dni"
        self.filters['obra_social'].label = "Obra Social "


    class Meta:
        model = Paciente
        fields = ['user__first_name', 'user__last_name', 'dni', 'obra_social', ]

class EstudioFilter(django_filters.FilterSet):

    #día = DateFilter(field_name='turno__date')
    #hora = TimeFilter(field_name='turno__timeFrom')
    #doctor = CharFilter(field_name='doctor')
    #paciente = CharFilter(field_name='paciente')
    #tipo = CharFilter(field_name='tipo')
    turno__date = DateFilter("turno__date", widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }))
    #turno__timeFrom = DateFilter("turno__timeFrom", widget=forms.TimeInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        super(EstudioFilter, self).__init__(*args, **kwargs)
        self.filters['tipo__especialidad'].label = "Especialidad "
        #self.filters['tipo__name'].label = "Estudio "
        self.filters['paciente'].label = "Paciente "
        self.filters['doctor'].label = "Médico "
        self.filters['turno__date'].label = "Día "
        #self.filters['turno__timeFrom'].label = "Hora"


    class Meta:
        model = Estudio
        fields = ['tipo__especialidad', 'paciente', 'doctor','turno__date'] #'turno__timeFrom'

class TurnoFilter(django_filters.FilterSet):

    date = DateFilter("date", widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }))


    def __init__(self, *args, **kwargs):
        super(TurnoFilter, self).__init__(*args, **kwargs)
        #self.filters['estudio__paciente'].label = "Paciente "
        self.filters['estudio__doctor'].label = "Médico "
        self.filters['date'].label = "Día "



    class Meta:
        model = Turno
        fields = [ 'estudio__doctor','date'] #'turno__timeFrom'


class TurnoPacienteFilter(django_filters.FilterSet):

    date = DateFilter("date", widget=forms.DateInput(
        attrs={
            'class': 'datepicker'
        }))

    def __init__(self, *args, **kwargs):
        super(TurnoPacienteFilter, self).__init__(*args, **kwargs)
        # self.filters['timeFrom'].label = "Hora "
        self.filters['estudio__doctor'].label = "Médico "
        self.filters['estudio__tipo__especialidad'].label = "Especialidad "
        self.filters['date'].label = "Día "
        # self.filters['turno__timeFrom'].label = "Hora"

    class Meta:
        model = Turno
        fields = ['estudio__tipo__especialidad','estudio__doctor', 'date']  # 'turno__timeFrom'

class EstudioPacienteFilter(django_filters.FilterSet):


    turno__date = DateFilter("turno__date", widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }))

    def __init__(self, *args, **kwargs):
        super(EstudioPacienteFilter, self).__init__(*args, **kwargs)
        self.filters['tipo__especialidad'].label = "Especialidad "
        #self.filters['tipo__name'].label = "Estudio "
        self.filters['doctor'].label = "Médico "
        self.filters['turno__date'].label = "Día "
        #self.filters['turno__timeFrom'].label = "Hora"


    class Meta:
        model = Estudio
        fields = ['tipo__especialidad', 'doctor','turno__date'] #'turno__timeFrom'


class TurnoMedicoFilter(django_filters.FilterSet):

    date = DateFilter("date", widget=forms.DateInput(
            attrs={
                'class': 'datepicker'
            }))


    def __init__(self, *args, **kwargs):
        super(TurnoMedicoFilter, self).__init__(*args, **kwargs)
        self.filters['estudio__paciente'].label = "Paciente "
        #self.filters['estudio__doctor'].label = "Médico "
        self.filters['date'].label = "Día "



    class Meta:
        model = Turno
        fields = ['estudio__paciente','date'] #'turno__timeFrom'