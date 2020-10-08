from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Paciente, Doctor, Estudio, Especialidad, Obra_social
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView, UpdateView
from .forms import SignUpFormMedico, SignUpFormPaciente
from django.db import transaction
from django.contrib.auth.models import Group



def index(request):
    # chequeo si el user pertenece a un grupo y en base a eso defino si esta autorizado o no
    # lo mando al template para chequear que pueve ver ahi también
    is_authorized = request.user.groups.filter(name='Medicos').exists()
    # exist se aplica a una colección por eso uso filter, con get no funciona.
    """
        Función vista para la página inicio del sitio.
    """
    num_medicos = Doctor.objects.all().count()
    num_pacientes = Paciente.objects.all().count()
    num_estudios = Estudio.objects.all().count()

    context = {
        'num_medicos': num_medicos,
        'num_pacientes': num_pacientes, 
        'num_estudios': num_estudios,
        'is_authorized': is_authorized
    }

    return render(request, 'index.html', context)

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


# @login_required en vez de usar esto chequeamos si el user pertenece a un grupo y mandamos
# el si o no por el context - mas facil asi parece
def medicos(request):
    """
        Función vista para la página inicio del sitio.
    
    medicos = doctor.objects.all()
    return render(request, 'medicos.html', context = {'medicos':medicos})
    """
    return HttpResponse('en construccion')


def signup_medico(request):
    is_authorized = request.user.groups.filter(name='Medicos').exists()
    if is_authorized:
        if request.method == 'POST':
            # Create a form instance from POST data.
            form = SignUpFormMedico(request.POST)
            if form.is_valid():
                # Save a new User object from the form's data.
                new_user = form.save()
                # new_user.refresh_from_db()  # load the profile instance created by the signal - no estoy seguro que sea necesario
                # estoy probando sin esto y por ahora va bien
                matricula_form = form.cleaned_data.get('matricula') # agarra por el name del input, no mira el id
                especialidad_form = form.cleaned_data.get('especialidad')
                if Especialidad.objects.filter(name=especialidad_form).exists():
                    especialidad = Especialidad.objects.get(name=especialidad_form)
                    # new_user.save() # verificar si hace falta guardar de nuevo
                    new_doctor = Doctor(matricula=matricula_form, user=new_user)
                    new_doctor.save()
                    new_doctor.especialidad.add(especialidad) 
                    new_doctor.save()
                    # me paso que necesitaba guardar antes de agregar especialidades, anda pero verificar
                    # si es necesario el codigo restante, talvez no lo sea
                    # doctor.refresh_from_db()
                    # doctor.especialidad.add(especialidad) 
                    
                    # a todo esto hay que cambiar en la vista que te deje dar de alta un medio
                    # con mas de 1 especialidad
                else:
                    print("especialidad no existe")
                # new_user.save() # no hace falta guardar devuelta el usuario al final de todo x ahora aparentemente
                return redirect('index')
            else:
                # falta agregar error por si el form es invalid
                pass
        else:
            # envio las especialidades al front para mostrarlas en el desplegable del alta
            # tambien mando el nivel de autorizacion para ver ver si puede o no ver la vista, etc
            especialidades = Especialidad.objects.order_by('name')
            context = { 
                'especialidades': especialidades, 
                'is_authorized': is_authorized
            }       
        return render(request, 'signup_medico.html', context)
    # direccionar a una url y hacer una vista de que no tiene permisos
    return HttpResponse('no estas autorizado - en construccion')

# def signup_medico2(request):
#     is_authorized = request.user.groups.filter(name='Medicos').exists()
#     if is_authorized:
#         if request.method == 'POST':
#             # Create a form instance from POST data.
#             formUser = SignUpForm(request.POST)
#             formDoctor = DoctorForm(request.POST)
#             if formUser.is_valid() and formDoctor.is_valid():
#                 # Save a new User object from the form's data.
#                 new_user = formUser.save()
#                 new_doctor = formDoctor.save()

#                 # a todo esto hay que cambiar en la vista que te deje dar de alta un medio
#                 # con mas de 1 especialidad

#                 print("especialidad no existe")
#                 # new_user.save() # no hace falta guardar devuelta el usuario al final de todo x ahora aparentemente
#                 return redirect('index')
#             else:
#                 # falta agregar error por si el form es invalid
#                 pass
#         else:
#             context = { 
#                 'formUser': SignUpForm(),
#                 'formDoctor': DoctorForm(),
#                 'is_authorized': is_authorized
#             }       
#         return render(request, 'signup_medico.html', context)
#     # direccionar a una url y hacer una vista de que no tiene permisos
#     return HttpResponse('no estas autorizado - bajo construcción todavia')

# los mismos comentarios de antes aplican aca asi que no los pongo
def signup_paciente(request):
    is_authorized = request.user.groups.filter(name='Medicos').exists()
    if is_authorized:
        if request.method == 'POST':
            # Create a form instance from POST data.
            form = SignUpFormPaciente(request.POST)
            print(form.errors)
            if form.is_valid():
                new_user = form.save()
                # new_user.refresh_from_db()  
                numero_telefono_form = form.cleaned_data.get('phone_number') 
                dni_form = form.cleaned_data.get('dni')
                date_of_birth_form = form.cleaned_data.get('date_of_birth')
                obra_social_form = form.cleaned_data.get('obra_social')
                if Obra_social.objects.filter(name=obra_social_form).exists():
                    grupo = Group.objects.get(name='Pacientes')
                    new_user.groups.add(grupo)
                    new_user.save()
                    paciente = Paciente(dni=dni_form, date_of_birth=date_of_birth_form, phone_number=numero_telefono_form, user=new_user)
                    #paciente.save()
                    #paciente.refresh_from_db()
                    paciente.obra_social = Obra_social.objects.get(name=obra_social_form)
                    paciente.save()
                    # doctor.save()
                    # new_user.save()
                    return redirect('index')  
                # print(form.errors) # muestra errores si el form es invalido
            else:
                # invalid form
                pass
        else:
            obras_sociales = Obra_social.objects.order_by('name')
            context = {
                'obras_sociales': obras_sociales,
                'is_authorized': is_authorized
            }
            return render(request, 'signup_paciente.html', context)
    else: 
        return HttpResponse('no estas autorizado - bajo construcción todavia')