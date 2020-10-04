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
from .forms import SignUpForm, MedicoProfileForm
from django.db import transaction


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

# def signup_medico(request):
#     especialidades = Especialidad.objects.order_by('name')
#     context = {
#         'especialidades': especialidades
#     }
#     print('0')
#     if request.method == 'POST':
#         form = MedicoSignUpFrom(request.POST)
#         print("0.1")
#         if form.is_valid():
#             user = form.save()
#             # user.refresh_from_db()  # load the profile instance created by the signal 
#             user.save()  
#             especialidad_form = form.cleaned_data.get('especialidad')
#             matricula_form = form.cleaned_data.get('matricula')
#             print('1')
#             #user.save()
#             doctor = Doctor(matricula= matricula_form, user= user)
#             print("la especialidad es")
#             print(especialidad_form)
#             especialidad = Especialidad.objects.get(name=especialidad_form)
#             print('2')
            
#             doctor.save() # needs to have a value for field "id" before this many-to-many relationship can be used
#             doctor.especialidad.add(especialidad)
#             doctor.save()
#             print('3')
#             # Doctor(user=user, matricula= )
#             return redirect('index')
#         else:
#             print("form not valid")
#     # else:
#         # form = SignUpForm() esto seria creo por si si usamos django forms para mandarla en el cont
#         # pero no lo hacemos por ahora, simplemente porq no se como darle estilo bien sin romper las cosas
#         # especialidades = Especialidad.objects.order_by('name')
#         # context = {
#         #   'especialidades': especialidades
#         # }   
#     return render(request, 'signup_medico.html', context)


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


def signup_medico(request):
    if request.method == 'POST':
        # Create a form instance from POST data.
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save a new User object from the form's data.
            new_user = form.save()
            new_user.refresh_from_db()  # load the profile instance created by the signal
            matricula_form = form.cleaned_data.get('matricula') # agarra por el name del input, no mira el id
            print(matricula_form)
            especialidad_form = form.cleaned_data.get('especialidad')
            if Especialidad.objects.filter(name=especialidad_form).exists():
                print("especialdiad  form: ", especialidad_form)
                especialidad = Especialidad.objects.get(name=especialidad_form)
                print("especialidad: ", especialidad.name )
                new_user.save()
                new_user.save()
                doctor = Doctor(matricula=matricula_form, user=new_user)
                doctor.save()
                doctor.refresh_from_db()
                doctor.especialidad.add(especialidad)
                doctor.save()
            else:
                print("especialidad no existe")
            # new_user.save()
            return redirect('index')
    else:
        form = SignUpForm()
        especialidades = Especialidad.objects.order_by('name')
        context = {
          'especialidades': especialidades,
          'form': form
        }   
    return render(request, 'signup_medico.html', context)