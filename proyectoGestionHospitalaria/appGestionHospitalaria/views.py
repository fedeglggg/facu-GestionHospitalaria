from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import patient, doctor, estudio
from django.views import generic

# Create your views here.
@login_required
def index(request):
    """
        Función vista para la página inicio del sitio.
    """
    num_medicos = doctor.objects.all().count()
    num_pacientes = patient.objects.all().count()
    num_estudios = estudio.objects.all().count()

    return render(request, 'index.html', context ={'num_medicos':num_medicos, 'num_pacientes':num_pacientes, 'num_estudios':num_estudios})



def usuarios(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'latest_question_list': latest_question_list}
    #return render(request, 'appGestionHospitalaria/index.html', context)
    return render(request, 'appGestionHospitalaria/index.html')


class patientsListView(generic.ListView):
    model = patient
    paginate_by = 10

class patientDetailView(generic.DetailView):
    model = patient


