from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import *
from django.contrib.auth.models import Group, User
from .filters import *
from django.http import HttpResponseRedirect



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

def timefields_to_min(timefield):
    lista_num_str = str(timefield).split(':')
    lista_num_int = []
    
    for i in lista_num_str:
        numero = int(i)
        lista_num_int.append(numero)
    
    minutos = (lista_num_int[0]*60) + lista_num_int[1] + (lista_num_int[2]/60) # horas *60 y seg /60 y dejo todo en min
    
    return minutos

def operate_timefields(tf_inicial, tf_final, operation): 
    minutos_numero_inicial = timefields_to_min(tf_inicial)
    minutos_numero_final = timefields_to_min(tf_final)

    if (operation == 'suma'):
        return minutos_numero_final + minutos_numero_inicial 
    else:
        return minutos_numero_final - minutos_numero_inicial 

def hour_to_timefield(hora_number):
    hora = int(hora_number)
    # print('hora_number: ', hora_number)
    # print('hora: ', hora)
    if hora < 10:
        return ('0' + str(hora) + ':00:00')
    else:
        return (str(hora) + ':00:00')


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

    myFilter = PatientFilter(request.GET, queryset=paciente_list)
    paciente_list = myFilter.qs

    context = {
        'paciente_list': paciente_list,
        'myFilter': myFilter
    }
    return render(request, 'paciente_list.html', context)

def medico_detail(request, doctor_id):
    if not is_user_auth(request.user, ('secretarios','sarasa')):
        return redirect('error_acceso')

    try:
        doc = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404("El doctor no existe")

    
    if request.method == 'POST':   

        if request.POST.get('horarios') == '1':
            if request.POST.get('lunes'):
                dia = DiaJornada.objects.get(nombre='Lunes')
                hora_inicio = request.POST.get('lunes_from')
                hora_fin = request.POST.get('lunes_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin) 
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists() # get porq estamos haciendo 1 sola jornada por medico
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Lunes')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()

            
            if request.POST.get('martes'):
                dia = DiaJornada.objects.get(nombre='Martes')
                hora_inicio = request.POST.get('martes_from')
                hora_fin = request.POST.get('martes_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin)
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Martes')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()

            if request.POST.get('miercoles'):
                dia = DiaJornada.objects.get(nombre='Miércoles')
                hora_inicio = request.POST.get('miercoles_from')
                hora_fin = request.POST.get('miercoles_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin)
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Miércoles')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()
            
            if request.POST.get('jueves'):
                dia = DiaJornada.objects.get(nombre='Jueves')
                hora_inicio = request.POST.get('jueves_from')
                hora_fin = request.POST.get('jueves_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin)
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Jueves')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()
            
            if request.POST.get('viernes'):
                dia = DiaJornada.objects.get(nombre='Viernes')
                hora_inicio = request.POST.get('viernes_from')
                hora_fin = request.POST.get('viernes_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin)
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Viernes')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()
            
            if request.POST.get('sabado'):
                dia = DiaJornada.objects.get(nombre='Sábado')
                hora_inicio = request.POST.get('sabado_from')
                hora_fin = request.POST.get('sabado_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin)
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Sábado')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()
            
            if request.POST.get('domingo'):
                dia = DiaJornada.objects.get(nombre='Domingo')
                hora_inicio = request.POST.get('domingo_from')
                hora_fin = request.POST.get('domingo_to')
                hora_inicio = hour_to_timefield(hora_inicio)
                hora_fin = hour_to_timefield(hora_fin)
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
                if turno_jor:
                    turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                    turno_jor.horario_inicio = hora_inicio
                    turno_jor.horario_fin = hora_fin
                    turno_jor.save()
                else:
                    new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                    new_turno_jornada.save()
            else:
                dia = DiaJornada.objects.get(nombre='Domingo')
                turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia)
                if TurnoJornada.objects.filter(doctor=doc,dia=dia).exists():
                    for i in turno_jor:
                        # print('borrando la jornada:', i.dia.nombre, i.horario_inicio, i.horario_fin)
                        i.delete()

        if request.POST.get('especialidades') == '1':
            form = UpdateMedicoEspecialidadForm(request.POST)
            if form.is_valid():
                index = 0
                especialidades_que_ya_tiene = Especialidad.objects.filter(doctor=doc)
                for i in lista_especialidades_nombres:
                    # si el checkbox no se marco directamente no se manda y da falso aca
                    nombre = dict_especialidades[i]
                    especialidad = Especialidad.objects.get(name=nombre)
                    if form.cleaned_data.get(i):                    
                        if especialidad in especialidades_que_ya_tiene:                                                         
                            #print('el doc ya tiene la especialidad: ', especialidad.name)
                            pass
                        else:
                            #print('el doc no tiene la especialidad - agregandola...', especialidad.name)
                            doc.especialidad.add(especialidad)
                            doc.save()
                    else:
                        #print('falta la especialidad:', i)
                        if especialidad in especialidades_que_ya_tiene:
                            #print('el doctor posee la especialidad', especialidad.name, 'pero no esta tildada, borrando...')
                            doc.especialidad.remove(especialidad)
                    index = index + 1
    
    especialidades_que_ya_tiene = Especialidad.objects.filter(doctor=doc)
    especialidades = Especialidad.objects.all()
    turnos_jornada = TurnoJornada.objects.filter(doctor=doc)

    dias = DiaJornada.objects.all()
    context = {
        'turnos_jornada': turnos_jornada,
        'especialidades': especialidades,
        'doctor': doc
    }

    for i in especialidades:      
        if i.name in dict_especialidades_back:
            esp = dict_especialidades_back[i.name]
            if i in especialidades_que_ya_tiene:
                context.update({esp:'1'})
                # print(i, esp)
        else:
            # por ahora no pasa nada pero arreglarlo despues
            print('esto no debería pasar, hay especialidades cargadas que no estan en el form: ', i.name)

    for i in li_dias:
        dia = DiaJornada.objects.get(nombre=i)
        for x in turnos_jornada:
            if x.dia == dia:
                context.update({dia.nombre:x})

    return render(request, 'medico_detail.html', context)

# @login_required en vez de usar esto chequeamos si el user pertenece a un grupo y mandamos
# el si o no por el context - mas facil asi parece
def medicos(request):
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')
      
    doctores = Doctor.objects.order_by('matricula')

    myFilter = DoctorFilter(request.GET, queryset=doctores)
    doctores = myFilter.qs

    context = {
        'doctores': doctores,
        'myFilter': myFilter
    }
    return render(request, 'medico_list.html', context)

def turnos(request):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')
      
    if request.method == 'POST':
        turno_pk = request.POST.get('turno_id')
        try:
            turno = Turno.objects.get(pk=turno_pk)
            if request.POST.get('confirmar') == '1':
                tipo_estudio_name = request.POST.get('tipo_estudio_name')
                tipo_estudio = TipoEstudio.objects.filter(name=tipo_estudio_name)
                especialidad = turno.estudio.tipo.especialidad
                if tipo_estudio.exists():
                    for i in tipo_estudio:
                        if i.especialidad == especialidad:
                            print('el tipo de estudio ya existe. especialidad = ', i.especialidad.name, ' - tipo: ', i.name)
                            turno.estudio.tipo = i
                else:
                    print('no hay ningun tipo de estudio con ese nombre - creando nuevo ')
                    new_tipo_estudio = TipoEstudio(name=tipo_estudio_name,especialidad=especialidad)
                    new_tipo_estudio.save()
                    turno.estudio.tipo = new_tipo_estudio

                turno.estudio.confirmed = True
                turno.estudio.save()

            else:
                if request.POST.get('confirmar') == '0':
                    turno.estudio.delete()
                    
        except Turno.DoesNotExist:
            raise Http404("El turno no existe")


    turnos = Turno.objects.all()

    myFilter = TurnoFilter(request.GET, queryset=turnos)
    turnos = myFilter.qs

    #for i in turnos:
       # print(i.estudio.doctor.user.first_name)
       # #print(i.estudio.paciente.user.first_name)

    context = {
        'turnos': turnos,
        'myFilter': myFilter
    }
    return render(request, 'turno_list.html', context)

def turnos_paciente(request):
    if not is_user_auth(request.user, ('pacientes', 'sarasa')):
        return redirect('error_acceso')    
      
    if request.method == 'POST':
        turno_pk = request.POST.get('turno_id')
        try:
            turno = Turno.objects.get(pk=turno_pk)
        except Turno.DoesNotExist:
            raise Http404("El turno no existe")

        if request.POST.get('confirmar') == '0':
            print('borrando el turno:', turno.date)
            turno.estudio.delete()

    paciente = Paciente.objects.get(user=request.user)
    estudios = Estudio.objects.filter(paciente=paciente)

    # de aca salgo con la lista de turnos
    turnosPks = set()
    for i in estudios:
        turno_aux = Turno.objects.get(estudio=i)
        turnosPks.add(turno_aux.pk)

    turnosPaciente = Turno.objects.filter(pk__in = turnosPks)
    #aca seguilo vos
    myFilter = TurnoPacienteFilter(request.GET, queryset=turnosPaciente)
    turnos = myFilter.qs

    context = {
        'turnos': turnos,
        'myFilter': myFilter
    }
    return render(request, 'turno_list_paciente.html', context)

def turnos_medico(request):
    if not is_user_auth(request.user, ('medicos', 'sarasa')):
        return redirect('error_acceso')    
      
    if request.method == 'POST':
        turno_pk = request.POST.get('turno_id')
        try:
            turno = Turno.objects.get(pk=turno_pk)
        except Turno.DoesNotExist:
            raise Http404("El turno no existe")

    medico = Doctor.objects.get(user=request.user)
    estudios = Estudio.objects.filter(doctor=medico)

    # de aca salgo con la lista de turnos
    turnosPks = set()
    for i in estudios:
        turno_aux = Turno.objects.get(estudio=i)
        turnosPks.add(turno_aux.pk)

    turnosMedicos = Turno.objects.filter(pk__in = turnosPks)
    # 
    myFilter = TurnoMedicoFilter(request.GET, queryset=turnosMedicos)
    turnos = myFilter.qs

    #for i in turnos:
       # print(i.estudio.doctor.user.first_name)
       # #print(i.estudio.paciente.user.first_name)

    context = {
        'turnos': turnos,
        'myFilter': myFilter
    }
    return render(request, 'turno_list_medico.html', context)

def historiasMedicas(request):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')

    estudios = Estudio.objects.filter(confirmed=True)
    myFilter = EstudioFilter(request.GET, queryset=estudios)
    estudios = myFilter.qs

    context = {
        'estudios': estudios,
        'myFilter': myFilter
    }
    return render(request, 'historia_list.html', context)

def historias_medicas_pacientes(request):
    if not is_user_auth(request.user, ('pacientes', 'sarasa')):
        return redirect('error_acceso')

    paciente = Paciente.objects.get(user=request.user)
    estudios = Estudio.objects.filter(confirmed=True, paciente=paciente)

    # si podes hacer que el filter no muestre el campo de paciente:
    myFilter = EstudioPacienteFilter(request.GET, queryset=estudios)
    estudios = myFilter.qs
    print(myFilter)

    context = {
        'estudios': estudios,
        'myFilter': myFilter
    }
    return render(request, 'historia_list_paciente.html', context)

def handle_uploaded_file(f):
    with open('uploads/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def historia(request, estudio_id):
    if not is_user_auth(request.user, ('secretarios', 'pacientes', 'medicos', 'sarasa')):
       return redirect('error_acceso')

    try:
        estudio = Estudio.objects.get(pk=estudio_id)
    except Estudio.DoesNotExist:
        raise Http404("El estudio no existe")

    if request.method == 'POST':
        if request.POST.get('option') == 'tipo_estudio_name':
            tipo_estudio_name = request.POST.get('tipo_estudio_name')
            tipo_estudio = TipoEstudio.objects.filter(name=tipo_estudio_name)
            estudio_id = request.POST.get('estudio_id')

            try:
                estudio = Estudio.objects.get(pk=estudio_id)
                especialidad = estudio.tipo.especialidad
            except Estudio.DoesNotExist:
                raise Http404("error en la toma del objeto")

            if tipo_estudio.exists():
                for i in tipo_estudio:
                    if i.especialidad == especialidad:
                        print('el tipo de estudio ya existe. especialidad = ', i.especialidad.name, ' - tipo: ', i.name)
                        estudio.tipo = i
            else:
                print('no hay ningun tipo de estudio con ese nombre - creando nuevo tipo - especialidad:', especialidad.name, 'tipo nombre: ', tipo_estudio_name)
                new_tipo_estudio = TipoEstudio(name=tipo_estudio_name,especialidad=especialidad)
                new_tipo_estudio.save()
                estudio.tipo = new_tipo_estudio

            estudio.save()

        if request.POST.get('option') == 'diagnostic':
            diagnostic = request.POST.get('diagnostic')
            estudio.diagnostic = diagnostic
            estudio.save()

        if request.POST.get('option') == 'comments': 
            comments = request.POST.get('comments')
            estudio.comments = comments
            estudio.save()

        if request.POST.get('option') == 'estudio_file': 
            estudio_file_pk = int(request.POST.get('estudio_file_id'))
            try:
                estudio_file = EstudioFile.objects.get(pk=estudio_file_pk)
                estudio_file.delete()
            except Estudio.DoesNotExist:
                raise Http404("error en la toma del objeto")

        if request.POST.get('option') == 'descripcion_file':
            archivo = request.FILES['archivo']
            descripcion = request.POST.get('descripcion_file')
            estudio_file = EstudioFile(estudio=estudio, file=archivo, descripcion=descripcion )
            estudio_file.save()
            
       
    files = EstudioFile.objects.filter(estudio = estudio)
    context = {
        'estudio': estudio,
        'files': files
    }

    return render(request, 'historia_detail.html', context)

dict_especialidades = {
    'traumatologia': 'Traumatología',
    'clinica_medica': 'Clínica médica',
    'cardiologia': 'Cardiología',
    'dermatologia': 'Dermatología',
    'oftalmologia': 'Oftalmologia',
    'endocrinologia': 'Endocrinología',
    'ginecologia': 'Ginecología',
    'obstetricia': 'Obstetricia',
    'psicologia': 'Psicología',
    'diagnostico_por_imagenes': 'Diagnóstico por Imágenes',
    'nutricion': 'Nutrición',
    'pediatria': 'Pediatría',
    'psiquiatria': 'Psiquiatría',
    'neumonologia': 'Neumonología'
}

dict_especialidades_back = {
    'Traumatología': 'traumatologia',
    'Clínica médica': 'clinica_medica',
    'Cardiología': 'cardiologia',
    'Dermatología': 'dermatologia',
    'Oftalmologia': 'oftalmologia',
    'Endocrinología': 'endocrinologia',
    'Ginecología': 'ginecologia',
    'Obstetricia': 'obstetricia',
    'Psicología': 'psicologia',
    'Diagnóstico por Imágenes': 'diagnostico_por_imagenes',
    'Nutrición': 'nutricion',
    'Pediatría': 'pediatria',
    'Psiquiatría': 'psiquiatria',
    'Neumonología': 'neumonologia', 
}

lista_especialidades_nombres = [
    'traumatologia',
    'clinica_medica',
    'cardiologia',
    'dermatologia',
    'oftalmologia',
    'endocrinologia',
    'ginecologia',
    'obstetricia',
    'psicologia',
    'diagnostico_por_imagenes',
    'nutricion', 
    'pediatria',
    'psiquiatria',
    'neumonologia',
]

def signup_medico(request):
    # le damos a is_auth los grupos permitidos en la vista
    # is auth devuelve true si el usuario tiene permisos en la vista
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')

    form = SignUpFormMedico(request.POST)
    # si el usuario esta autorizado a ver la vista sigue
    if request.method == 'POST':
        # Create a form instance from POST data.
        # form = SignUpFormMedico(request.POST)
        if form.is_valid(): # sino el cleaned data get no funca - dependiendo del tipo de form chequea que las instancais no sea repetidas en la bd también
            print(request.POST) # para ver la post data
            # Save a new User object from the form's data.
            new_user = form.save()
            grupo = Group.objects.get(name='medicos')
            new_user.groups.add(grupo)
            # new_user.refresh_from_db()  # load the profile instance created by the signal - 
            # no estoy seguro que sea necesario, estoy probando sin esto y por ahora va bien
            
            matricula_form = form.cleaned_data.get('matricula') # agarra por el name del input, no mira el id 
          
            # new_user.save() # verificar si hace falta guardar de nuevo
            new_doctor = Doctor(matricula=matricula_form, user=new_user)
            new_doctor.save()

            # añadiendo las especialidades al doctor
            index = 0
            for i in lista_especialidades_nombres:
                # si el checkbox no se marco directamente no se manda y da falso aca
                if form.cleaned_data.get(i):
                    nombre = dict_especialidades[i]
                    especialidad = Especialidad.objects.get(name=nombre) 
                    new_doctor.especialidad.add(especialidad)
                    print('especialidad seleccionada:', especialidad.name)
                index = index + 1

            new_user.save() 
            new_doctor.save()
            # me paso que necesitaba guardar antes de agregar especialidades, anda pero verificar
            # si es necesario el codigo restante, talvez no lo sea
            # doctor.refresh_from_db()
            # doctor.especialidad.add(especialidad) 
            # new_user.save() # no hace falta guardar devuelta el usuario al final de todo x ahora aparentemente

            # hardcoded por ahora, habría que buscar alguna forma de tomar la url de urls.py que es dinamica en vez de poner /sigup/med...
            return HttpResponseRedirect('/medico/' + str(new_doctor.pk) + '/turnos/')
            # return render(request, 'signup_medico_turnos.html', context)
        else:
            # falta agregar error por si el form es invalid
            print('form fail errors:')
            print(form.errors)
            context = { 
                'especialidades': Especialidad.objects.order_by('name'),
                'form': form
            }  
            return render(request, 'signup_medico.html', context)
            
    else:
        # envio las especialidades al front para mostrarlas en el desplegable del alta
        context = { 
            'especialidades': Especialidad.objects.order_by('name')
        }       
        return render(request, 'signup_medico.html', context)

li_dias = [
    'Lunes',
    'Martes',
    'Miércoles',
    'Jueves',
    'Viernes',
    'Sábado',
    'Domingo'
]

def medico_turnos(request, doctor_id):
    # le damos a is_auth los grupos permitidos en la vista
    # is auth devuelve true si el usuario tiene permisos en la vista
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')

    try:
        doc = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404("El doctor no existe")

    # si el usuario esta autorizado a ver la vista sigue
    if request.method == 'POST':   
        # añadiendo los horarios del medico
        

        if request.POST.get('lunes'):
            dia = DiaJornada.objects.get(nombre='Lunes')
            hora_inicio = request.POST.get('lunes_from')
            hora_fin = request.POST.get('lunes_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin) 
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists() # get porq estamos haciendo 1 sola jornada por medico
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()
        
        if request.POST.get('martes'):
            dia = DiaJornada.objects.get(nombre='Martes')
            hora_inicio = request.POST.get('martes_from')
            hora_fin = request.POST.get('martes_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin)
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()

        if request.POST.get('miercoles'):
            dia = DiaJornada.objects.get(nombre='Miércoles')
            hora_inicio = request.POST.get('miercoles_from')
            hora_fin = request.POST.get('miercoles_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin)
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()
        
        if request.POST.get('jueves'):
            dia = DiaJornada.objects.get(nombre='Jueves')
            hora_inicio = request.POST.get('jueves_from')
            hora_fin = request.POST.get('jueves_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin)
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()
        
        if request.POST.get('viernes'):
            dia = DiaJornada.objects.get(nombre='Viernes')
            hora_inicio = request.POST.get('viernes_from')
            hora_fin = request.POST.get('viernes_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin)
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()
        
        if request.POST.get('sabado'):
            dia = DiaJornada.objects.get(nombre='Sábado')
            hora_inicio = request.POST.get('sabado_from')
            hora_fin = request.POST.get('sabado_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin)
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()

        
        if request.POST.get('domingo'):
            dia = DiaJornada.objects.get(nombre='Domingo')
            hora_inicio = request.POST.get('domingo_from')
            hora_fin = request.POST.get('domingo_to')
            hora_inicio = hour_to_timefield(hora_inicio)
            hora_fin = hour_to_timefield(hora_fin)
            turno_jor = TurnoJornada.objects.filter(doctor=doc,dia=dia).exists()
            if turno_jor:
                turno_jor = TurnoJornada.objects.get(doctor=doc,dia=dia)
                turno_jor.horario_inicio = hora_inicio
                turno_jor.horario_fin = hora_fin
                turno_jor.save()
            else:
                new_turno_jornada = TurnoJornada(doctor=doc, dia=dia, horario_inicio=hora_inicio, horario_fin=hora_fin)
                new_turno_jornada.save()
        return redirect('index')

    turnos_jornada = TurnoJornada.objects.filter(doctor=doc)
    dias = DiaJornada.objects.all()
    context = {
        'doctor': doc,
        'turnos_jornada': turnos_jornada,
    }

    for i in li_dias:
        dia = DiaJornada.objects.get(nombre=i)
        for x in turnos_jornada:
            if x.dia == dia:
                context.update({dia.nombre:x})

    return render(request, 'medico_turnos.html', context)  
            

# todos los comentarios de signup_medico aplican aca
# def signup_pacienteOld(request):
#     if not is_user_auth(request.user, ('secretarios')):
#         return redirect('error_acceso')

#     form = SignUpFormPaciente(request.POST)
#     if request.method == 'POST':
#         # form = SignUpFormPaciente(request.POST)
#         print(form.errors)
#         if form.is_valid():
#             new_user = form.save() 
#             numero_telefono_form = form.cleaned_data.get('phone_number') 
#             dni_form = form.cleaned_data.get('dni')
#             date_of_birth_form = form.cleaned_data.get('date_of_birth')
#             obra_social_form = form.cleaned_data.get('obra_social')
#             grupo = Group.objects.get(name='pacientes')
#             new_user.groups.add(grupo)
#             new_user.save()
#             paciente = Paciente(dni=dni_form, date_of_birth=date_of_birth_form, phone_number=numero_telefono_form, user=new_user)
#             paciente.obra_social = Obra_social.objects.get(name=obra_social_form)
#             paciente.save()
#             return redirect('index')  
#         else:
#             context = { 
#                 'obras_sociales': Obra_social.objects.order_by('name'),
#                 'form': form
#             }  
#             return render(request, 'signup_paciente.html', context)
#     else:
#         context = {
#             'obras_sociales': Obra_social.objects.order_by('name'),
#         }
#         return render(request, 'signup_paciente.html', context)

def signup_paciente(request):
    if not is_user_auth(request.user, ('secretarios')):
        return redirect('error_acceso')

    form = SignUpFormPaciente(request.POST)
    form_paciente = PacienteForm(request.POST)
    if request.method == 'POST':
        # form = SignUpFormPaciente(request.POST)
        print(form.errors)
        print(form_paciente.errors)
        if form.is_valid() and form_paciente.is_valid():
            new_user = form.save() 
            grupo = Group.objects.get(name='pacientes')
            new_user.groups.add(grupo)
            new_user.save()

            new_paciente = form_paciente.save(commit=False)
            dni = Obra_social.objects.get(name=form_paciente.cleaned_data.get('dni'))

            obra_social = Obra_social.objects.get(name=form_paciente.cleaned_data.get('obra_social'))
            new_paciente.obra_social = obra_social 
            new_paciente.user = new_user           
            new_paciente.save()

            return redirect('index')  
        else:
            context = { 
                'obras_sociales': Obra_social.objects.order_by('name'),
                'form': form,
                'form_paciente': form_paciente
            }  
            return render(request, 'signup_paciente.html', context)
    else:
        context = {
            'obras_sociales': Obra_social.objects.order_by('name'),
        }
        return render(request, 'signup_paciente.html', context)

def create_turno_1(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('/accounts/login')
    
    # El post directamente lo hace en /2 - esta seteado desde el front
    if request.method == 'GET':
        context = {
            'especialidades': Especialidad.objects.all()
        }
        return render(request, 'create_turno_1.html', context)
    else:
        return redirect('error_acceso')

def create_turno_2(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')

    if request.method == 'GET':
        form = EspecialidadForm(request.GET)
        if form.is_valid(): 
            especialidad_name = form.cleaned_data.get('name')
            especialidad = Especialidad.objects.get(name=especialidad_name)
            doctores = Doctor.objects.filter(especialidad=especialidad)
            # tipoEstudios = TipoEstudio.objects.filter(especialidad=especialidad)
            context = {
                'doctores': doctores,
                'especialidad': especialidad,
                # 'tipoEstudios': tipoEstudios,
                # 'lista_pacientes': Paciente.objects.all()

            }
            return render(request, 'create_turno_2.html', context)
        else:
            return redirect('error_acceso')
    else:
        return redirect('error_acceso')

def create_turno_3(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')
    
    if request.method == 'GET':
        form = DoctorMatriculaForm(request.GET) # Me quedo con la matricula por el value dentro del select
        if form.is_valid():
            especialidad_name = form.cleaned_data.get('especialidad') 
            especialidad = Especialidad.objects.get(name=especialidad_name)
            matricula = form.cleaned_data.get('matricula')
            doctor = Doctor.objects.get(matricula=matricula)

            context = {
                # 'tipo_estudios': TipoEstudio.objects.all(),
                'lista_pacientes': Paciente.objects.all(),
                'especialidad': especialidad,
                'doctor': doctor 
            }
        
            return render(request, 'create_turno_3.html', context)

dict_dias = {
    '0': 'Lunes',
    '1': 'Martes',
    '2': 'Miércoles',
    '3': 'Jueves',
    '4': 'Viernes',
    '5': 'Sábado',
    '6': 'Domingo'
}


def create_turno_4(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')     

    if request.method == 'GET':
        doctorForm = DoctorMatriculaForm(request.GET)
        turnoForm = TurnoDateForm(request.GET)
        if turnoForm.is_valid() and doctorForm.is_valid():
            mpt = 60 # mintuos por turno usado mas adelante - se puede cambiar esto y modifica todo facil
            date = turnoForm.cleaned_data.get('date')  
            dia = dict_dias[str(date.weekday())]  # date.weekday() traduce date a dias -> 0 es lunes y 7 domingo 
            matricula = doctorForm.cleaned_data.get('matricula')
            doctor = Doctor.objects.get(matricula=matricula)
            turnos_de_jornadas = TurnoJornada.objects.filter(doctor=doctor)

            # creacion de lista de horarios de la jornada de ese dia del doctor (a mas posiciones mas veces va a trabajar en un horario)
            atiende_ese_dia = False
            turnos_jornada = []
            for i in turnos_de_jornadas:
                if i.dia.nombre == dia:
                    atiende_ese_dia = True
                    turnos_jornada.append(i)

           # cuantos turnos tiene en cada uno de los horarios de esa jornada
           # ej [10,2] sería que puede atender 10 veces en el primer turno del dia y 2 veces en el segundo
           # haría doble turno en este caso 
            cantidad_de_turnos = []
            for i in turnos_jornada:
                a = operate_timefields(i.horario_inicio, i.horario_fin, 'resta')
                a = int(a//mpt)
                cantidad_de_turnos.append(a) # total de min de turnos / m por turno

            # agarro los turnos tomados de ese dia
            # y los transformo en min (los date) 
            turnos_tomados_todos = Turno.objects.filter(date=date) # turnos de la fecha
            estudios = Estudio.objects.filter(doctor=doctor)
            turnos_tomados = [] # va a contener turnos de ese dia Y turnos de ese medico
            aux = []
            for i in estudios:
                aux = turnos_tomados_todos.filter(estudio=i)
                for i in aux:
                    turnos_tomados.append(i)
           
            turnos_tomados_minutos = []
            for i in turnos_tomados:
                turnos_tomados_minutos.append(timefields_to_min(i.timeFrom))

            # va a listar todos los turnos en minutos de la jornada que tiene disponibles
            # ej [600, 700] serian 600/60 = 6am el otro las 7am, etc
            turnos_disponibles = []
            index_i = 0
            for i in cantidad_de_turnos:
                base = timefields_to_min(turnos_jornada[index_i].horario_inicio)
                index_i = index_i + 1
                for x in range(i):
                    horario = base + x*mpt
                    aux = False

                    # chequea si hay al menos 1 turno tomado que es = a un horario que daria de los turnos
                    for j in turnos_tomados_minutos:
                        if j == horario:
                            aux = True
                            print('se cansela un turno al ya estar tomado')
                            
                    if not aux:
                        horario = int(horario)
                        turnos_disponibles.append(horario)

            print('turnos disponibles:', turnos_disponibles)
            # conversión a de min a horas y en formato str para poder publicar en el template
            index_i = 0
            lista_turnos = []
            for i in turnos_disponibles:
                horas = i/60
                minutos = int(horas % 1 * 60)
                if minutos == 0:
                    minutos = '00'
                else:
                    minutos = round(minutos,2)
                horas = int(horas)
                if horas >= 12:
                   lista_turnos.append(str(horas) + ':' + str(minutos) + ' pm')
                else:
                    lista_turnos.append(str(horas) + ':' + str(minutos) + ' am')
                index_i = index_i + 1

            date = str(date)
            dni = turnoForm.cleaned_data.get('dni')
            paciente = Paciente.objects.get(dni=dni)
            especialidad = doctorForm.cleaned_data.get('especialidad')
            especialidad = Especialidad.objects.get(name=especialidad)
            context = {
                'turnos_disponibles': lista_turnos,
                'doctor': doctor,
                'paciente': paciente,
                'especialidad': especialidad,
                'date': date
            }
            return render(request, 'create_turno_4.html', context) 
        else:
            print('-------------------------------')
            print('errores del form de doctor')
            print(doctorForm.errors)
            print('errores del form de turno')
            print(turnoForm.errors)
            print('-------------------------------')
            return redirect('error_acceso')
    else:
        turno_form = TurnoForm(request.POST)
        if turno_form.is_valid():
            dni = turno_form.cleaned_data.get('dni')
            matricula = turno_form.cleaned_data.get('matricula')
            date = turno_form.cleaned_data.get('date')
            especialidad_name = turno_form.cleaned_data.get('especialidad')
            especialidad = Especialidad.objects.get(name=especialidad_name)
            turno = turno_form.cleaned_data.get('turno')
            paciente = Paciente.objects.get(dni=dni)
            doctor = Doctor.objects.get(matricula=matricula)
            tipo = TipoEstudio.objects.get(name='Consulta',especialidad=especialidad) # todos los turnos crean un estudio de tipo consulta al inicio y despues se cambia
            # Mas adelante hacemos si va a cambiar el tipo de estudio y no tiene especialidad asignada tonces que cree un nuevo tipo estudio con el nobmre correspondiente y su especialidad
            # ya que si solamente le asignamos al tipo estudio una especialidad y cambiar de nombre al ya creado tiraria error la linea de arriba
            aux_1 = str(turno).split(' ')
            aux_2 = aux_1[0].split(':')

            # conversion a timefield
            if int(aux_2[0]) >= 10:
                if str(int(aux_2[1])) == '0':
                    time = str(int(aux_2[0])) + ':00:00'
                else:
                    time = str(int(aux_2[0])) + ':' + str(int(aux_2[1])) + ':00'
            else:
                if str(int(aux_2[1])) == '0':
                    time = '0' + str(int(aux_2[0])) + ':00:00'
                else:
                    time = '0' + str(int(aux_2[0])) + ':' + str(int(aux_2[1])) + ':00'

            new_estudio = Estudio(paciente=paciente, doctor=doctor, tipo=tipo)
            new_estudio.save()
            new_turno = Turno(estudio=new_estudio, date=date, timeFrom=time)
            new_turno.save()
            return redirect('index')
        else:
            print('error')
            print(turno_form.errors)

    