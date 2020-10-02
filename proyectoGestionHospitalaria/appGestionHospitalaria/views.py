from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Paciente, Doctor, Estudio, Especialidad
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView, UpdateView
from .forms import SignUpForm, MedicoSignUpFrom



# Create your views here.
def index(request):
    """
        Función vista para la página inicio del sitio.
    """
    num_medicos = Doctor.objects.all().count()
    num_pacientes = Paciente.objects.all().count()
    num_estudios = Estudio.objects.all().count()

    return render(request, 'index.html', context ={'num_medicos':num_medicos, 'num_pacientes':num_pacientes, 'num_estudios':num_estudios})

# <int:paciente_id>/ es mandado como parametro
# si no lo agrego en la funcion de abajo genera error
def paciente(request, paciente_id):
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
    except Paciente.DoesNotExist:
        raise Http404("El paciente no existe")
    return render(request, 'paciente_detail.html', {'paciente': paciente})

def pacientes(request):
    paciente_list = Paciente.objects.order_by('dni')
    context = {
        'paciente_list': paciente_list
    }
    return render(request, 'paciente_list.html', context)

def signup_paciente(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Inicio')
    else:
        form = SignUpForm()
    return render(request, 'signup_paciente.html', {'form': form})

def signup_medico(request):
    if request.method == 'POST':
        form = MedicoSignUpFrom(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('index')
    else:
        # form = SignUpForm()
        especialidades = Especialidad.objects.order_by('name')
        num = Especialidad.objects.all().count()
        print(num)
        context = {
            'especialidades': especialidades
        }
        # context = {
        #     'form': form
        #     'especialidades': especialidades 
        # }
    return render(request, 'signup_medico.html', context)

# @login_required
# def medicosSignup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('Inicio')
#     else:
#         form = SignUpForm()
#     return render(request, 'medicosSignup.html', {'form': form})

@login_required
def medicos(request):

    """
        Función vista para la página inicio del sitio.
    
    medicos = doctor.objects.all()
    return render(request, 'medicos.html', context = {'medicos':medicos})
    """
    return HttpResponse('lala')