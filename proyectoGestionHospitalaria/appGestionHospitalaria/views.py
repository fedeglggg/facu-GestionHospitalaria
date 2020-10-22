from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Paciente, Doctor, Estudio, Especialidad, Obra_social, Turno, TipoEstudio
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
from django.http import Http404
from django.views.generic import CreateView, UpdateView
from .forms import SignUpFormMedico, SignUpFormPaciente, CreateFormTurno
from django.db import transaction
from django.contrib.auth.models import Group, User


# funcion que valida los permisos de una vista en base a los grupos a los que pertenece el usuario
# y los grupos que permite la vista
def is_user_auth(user, valid_groups):
    # staff siempre tiene permiso
    if user.is_staff:
        return True
    
    # probé de otras formas que en teoría serian mas optimas pero no me dejó
    # valiar que hay al menos 1 grupo de los cuales el usuario pertenece y es valido
    for group in valid_groups:
        if user.groups.filter(name=group).exists():
            return True
    return False
  
def error_acceso(request):
    # se podría tirar algo aca, el proble es que al desloguear te habría que redirigirlo, 
    # sino deslogueo y quedo en una vista que necesita permisos y automaticamente despues
    #  de desloguear se activaria esta vista
    return redirect('index')
    # return HttpResponse('usted no tiene permiso para solicitar esta pagina - bajo construcción')    

def index(request):
    # chequeo si el user pertenece a un grupo y en base a eso defino si esta autorizado o no
    # lo mando al template para chequear que pueve ver ahi también
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
    }

    return render(request, 'index.html', context)

# <int:paciente_id>/ es mandado como parametro
# si no lo agrego en la funcion de abajo genera error
def paciente(request, paciente_id):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
    except Paciente.DoesNotExist:
        raise Http404("El paciente no existe")
    return render(request, 'paciente_detail.html', {'paciente': paciente})

def pacientes(request):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')
    paciente_list = Paciente.objects.order_by('dni')
    context = {
        'paciente_list': paciente_list
    }
    return render(request, 'paciente_list.html', context)


# @login_required en vez de usar esto chequeamos si el user pertenece a un grupo y mandamos
# el si o no por el context - mas facil asi parece
def medicos(request):
    """
        Función vista para la página del listado de medicos.
    
    medicos = doctor.objects.all()
    return render(request, 'medicos.html', context = {'medicos':medicos})
    """
    return HttpResponse('en construccion')

def signup_medico(request):
    # le damos a is_auth los grupos permitidos en la vista
    # is auth devuelve true si el usuario tiene permisos en la vista
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')

    # si el usuario esta autorizado a ver la vista sigue
    if request.method == 'POST':
        # Create a form instance from POST data.
        form = SignUpFormMedico(request.POST)
        if form.is_valid():
            # Save a new User object from the form's data.
            new_user = form.save()
            grupo = Group.objects.get(name='medicos')
            new_user.groups.add(grupo)
            # new_user.refresh_from_db()  # load the profile instance created by the signal - 
            # no estoy seguro que sea necesario, estoy probando sin esto y por ahora va bien
            matricula_form = form.cleaned_data.get('matricula') # agarra por el name del input, 
            # no mira el id
            especialidad_form = form.cleaned_data.get('especialidad')
            # if Especialidad.objects.filter(name=especialidad_form).exists(): 
            # no hace falta chequear la especialidad porque la voy a buscar a la db antes de mostrarla
            especialidad = Especialidad.objects.get(name=especialidad_form)
            # new_user.save() # verificar si hace falta guardar de nuevo
            new_doctor = Doctor(matricula=matricula_form, user=new_user)
            new_doctor.save()
            new_doctor.especialidad.add(especialidad)
            new_user.save() 
            new_doctor.save()
            # me paso que necesitaba guardar antes de agregar especialidades, anda pero verificar
            # si es necesario el codigo restante, talvez no lo sea
            # doctor.refresh_from_db()
            # doctor.especialidad.add(especialidad) 
            
            # new_user.save() # no hace falta guardar devuelta el usuario al final de todo x ahora 
            # aparentemente
            return redirect('index')
        else:
            # falta agregar error por si el form es invalid
            pass
    else:
        # envio las especialidades al front para mostrarlas en el desplegable del alta
        context = { 
            'especialidades': Especialidad.objects.order_by('name')
        }       
        return render(request, 'signup_medico.html', context)

# todos los comentarios de signup_medico aplican aca
def signup_paciente(request):
    if not is_user_auth(request.user, ('medicos', 'sarasa')):
        return redirect('error_acceso')

    if request.method == 'POST':
        form = SignUpFormPaciente(request.POST)
        print(form.errors)
        if form.is_valid():
            new_user = form.save() 
            numero_telefono_form = form.cleaned_data.get('phone_number') 
            dni_form = form.cleaned_data.get('dni')
            date_of_birth_form = form.cleaned_data.get('date_of_birth')
            obra_social_form = form.cleaned_data.get('obra_social')
            grupo = Group.objects.get(name='pacientes')
            new_user.groups.add(grupo)
            new_user.save()
            paciente = Paciente(dni=dni_form, date_of_birth=date_of_birth_form, phone_number=numero_telefono_form, user=new_user)
            paciente.obra_social = Obra_social.objects.get(name=obra_social_form)
            paciente.save()
            return redirect('index')  
        else:
            # invalid form
            pass
    else:
        context = {
            'obras_sociales': Obra_social.objects.order_by('name'),
        }
        return render(request, 'signup_paciente.html', context)

def create_turno(request):
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')

    if request.method == 'POST':
        form = CreateFormTurno(request.POST)
        print(form.errors)
        if form.is_valid():
            estudio_name = form.cleaned_data.get('name')
            doctor = form.cleaned_data.get('doctor')
            paciente = Paciente.objects.get(pk=1) #Tendria que obtener la pk del usuario paciente que esta creando el turno
            secretary = User.objects.get(pk=1) #por ahora por defecto, se relaciona con un secretario (empiezo a dudar si es necesario)
            description = ''
            estudio1 = Estudio(type=estudio_name, doctor=doctor, paciente=paciente, secretary=secretary, description=description)
            estudio1.save() #Crea el estudio
            date = form.cleaned_data.get('date')
            timeFrom = form.cleaned_data.get('timeFrom')
            timeTo = timeFrom.replace(hour=(timeFrom.hour+estudio1.type.duration) % 24) #Suma la duracion de estudio
            turno = Turno(estudio=estudio1, date=date, timeFrom=timeFrom, timeTo=timeTo)
            turno.save() #Crea el turno a partir de ese estudio
            return redirect('index')
        else:
            # invalid form
            pass
    else:
        context = {
            'Tipo_Estudios': TipoEstudio.objects.all(),
            'ListaDoctores': Doctor.objects.all() #.filter(especialidad=TipoEstudio.especialidad)
        }
        return render(request, 'Create_Turno.html', context)