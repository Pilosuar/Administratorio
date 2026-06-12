from django.shortcuts import render, redirect
from .models import Alumno, Curso, Grupo, Inscripcion, EstatusInscripcion
from .forms import AlumnoForm, CursoForm, GrupoForm, InscripcionForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import os

#Renderiza la plantilla principal
def plantilla(request):
    return render(request, "plantilla.html")

###  A L U M N O S
#Muestra un formulario para crear un alumno
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES)
        #Si todos los campos son validados al enviar el formulario se guardan los datos
        if form.is_valid():
            form.save()
            #Redirecciona al listado de alumnos
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()

    return render(request, 'crear_alumno.html', {
        'form': form
    })

#Muestra un listado de todos los alumnos
def lista_alumnos(request):
    #Filtra mediante el buscador
    buscar = request.GET.get('buscar', '')
    #Busca los alumnos por los campos 'apellido_paterno', 'apellido_materno' y 'nombre'
    alumnos = Alumno.objects.prefetch_related(
        'inscripciones__grupo__curso'
    ).order_by('apellido_paterno', 'apellido_materno', 'nombre')
    #Filtra los alumnos con mas de un curso
    if buscar:
        alumnos = alumnos.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido_paterno__icontains=buscar) |
            Q(apellido_materno__icontains=buscar) |
            Q(escuela__icontains=buscar) |
            Q(inscripciones__grupo__curso__nombre__icontains=buscar) 
        ).distinct()

    paginator = Paginator(alumnos, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    return render(request, 'registro/lista_alumnos.html', {'page_obj': page_obj, 'buscar': buscar})

#Muestra los datos completos relacionados con el alumno
def detalle_alumno(request, pk):
    #Busca al alumno por su 'id' y muestra sus datos
    alumno = get_object_or_404(Alumno, pk=pk)
    return render(request, 'registro/detalle_alumno.html', {'alumno': alumno})

#Mustra el formulario con los datos registrados del alumno
def editar_alumno(request, pk):
    #Busca al alumno por su 'id' y muestra sus datos
    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES, instance=alumno)
        #Si todos los campos son validados al enviar el formulario se guardan los datos
        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request,'editar_alumno.html',{'form': form})

#Mustra una plantilla para confirmar la eliminacion
def eliminar_alumno(request, pk):

    alumno = get_object_or_404(Alumno, pk=pk)

    if request.method == 'POST':
        alumno.delete()
        return redirect('lista_alumnos')

    return render(request, 'eliminar_alumno.html', {'alumno': alumno})

### C U R S O S
#Muestra un listado de todos los cursos
def lista_cursos(request):
    #Obitiene todos los cursos
    cursos = Curso.objects.all()

    return render(request, 'lista_cursos.html', {'cursos': cursos})

#Muestra un formulario para crear un curso
def crear_curso(request):

    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cursos')
    else:
        form = CursoForm()

    return render(request, 'crear_curso.html', {'form': form})

#Mustra el formulario con los datos registrados del curso
def editar_curso(request, id):

    curso = get_object_or_404(Curso, pk=id)

    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()

            return redirect('lista_cursos')
    else:
        form = CursoForm(instance=curso)

    return render(request, 'editar_curso.html', {'form': form, 'curso': curso})

#Mustra una plantilla para confirmar la eliminacion
def eliminar_curso(request, id):

    curso = get_object_or_404(Curso, pk=id)

    if request.method == 'POST':
        curso.delete()
        return redirect('lista_cursos')

    return render(request, 'eliminar_curso.html', {'curso': curso})

### G R U P O S
#Muestra un listado de todos los grupos
def lista_grupos(request):

    grupos = Grupo.objects.all()

    return render(request, 'lista_grupos.html', {'grupos': grupos})

#Muestra un formulario para crear un alumno
def crear_grupo(request):

    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_grupos')
    else:
        form = GrupoForm()

    return render(request, 'crear_grupo.html', {'form': form})

#Mustra el formulario con los datos registrados del grupo
def editar_grupo(request, id):

    grupo = get_object_or_404(Grupo, pk=id)

    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect('lista_grupos')

    else:
        form = GrupoForm(instance=grupo)

    return render(request, 'editar_grupo.html', {'form': form, 'grupo': grupo})

#Mustra una plantilla para confirmar la eliminacion
def eliminar_grupo(request, id):

    grupo = get_object_or_404(Grupo, pk=id)

    if request.method == 'POST':
        grupo.delete()
        return redirect('lista_grupos')

    return render(request, 'eliminar_grupo.html', {'grupo': grupo})

### I N S C R I P C I O N E S
#Muestra un listado de todos las incripciones
def lista_inscripciones(request):
    #Verifica que la fecha actual sea menor a la fecha de baja sino actualiza el status a 'INACTIVO'    
    inscripciones_vencidas = Inscripcion.objects.filter(
        fecha_baja__isnull=False,
        fecha_baja__lte=date.today(),
        estatus=EstatusInscripcion.ACTIVO
    )

    for inscripcion in inscripciones_vencidas:

        inscripcion.estatus = EstatusInscripcion.INACTIVO
        inscripcion.save(update_fields=['estatus'])

        enviar_correo_fin_inscripcion(inscripcion)

    inscripciones = (
        Inscripcion.objects
        .select_related('alumno', 'grupo', 'grupo__curso'))

    return render(request, 'lista_inscripciones.html', {'inscripciones': inscripciones})

#Define la funcion con los datos a enviar en el correo
def enviar_correo_inscripcion(inscripcion):

    alumno = inscripcion.alumno

    destinatarios = []

    if alumno.madre_correo:
        destinatarios.append(alumno.madre_correo)

    if alumno.padre_correo:
        destinatarios.append(alumno.padre_correo)

    if alumno.otro_correo:
        destinatarios.append(alumno.otro_correo)

    # Eliminar duplicados
    destinatarios = list(set(destinatarios))
    if not destinatarios:
        return

    asunto = "Confirmación de inscripción"

    mensaje = f"""
        Estimado padre o tutor:

        Se ha registrado correctamente la inscripción de:

        Alumno: {alumno}
        Curso: {inscripcion.grupo.curso.nombre}
        Grupo: {inscripcion.grupo.nombre}
        Fecha de inscripción: {inscripcion.fecha_inscripcion}
        Fecha de finalización: {inscripcion.fecha_baja}

        Se adjuntan los documentos correspondientes.

        Atentamente.
        Centro edicativo Pädi
        """

    correo = EmailMessage(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        destinatarios
    )

    #Adjunta contrato subido
    if inscripcion.contrato_pdf:
        correo.attach_file(
            inscripcion.contrato_pdf.path
        )

    #Adjunta reglamento
    reglamento = os.path.join(
        settings.BASE_DIR,
        'media',
        'documentos',
        'Reglamento.pdf'
    )

    if os.path.exists(reglamento):
        correo.attach_file(reglamento)

    correo.send()

#Envia correo cuando llega el fin de la inscripción
def enviar_correo_fin_inscripcion(inscripcion):

    alumno = inscripcion.alumno

    destinatarios = []

    if alumno.madre_correo:
        destinatarios.append(alumno.madre_correo)

    if alumno.padre_correo:
        destinatarios.append(alumno.padre_correo)

    if alumno.otro_correo:
        destinatarios.append(alumno.otro_correo)

    destinatarios = list(set(destinatarios))

    if not destinatarios:
        return

    asunto = "Finalización de inscripción"

    mensaje = f"""
        Estimado padre o tutor:

        Le informamos que ha concluido el periodo de inscripción del alumno:

        Alumno: {alumno}
        Curso: {inscripcion.grupo.curso.nombre}
        Grupo: {inscripcion.grupo.nombre}

        Fecha de finalización:
        {inscripcion.fecha_baja}

        Si desea renovar la inscripción o recibir más información,
        favor de comunicarse con nosotros.

        Atentamente.
        Centro Educativo Pädi
        """

    correo = EmailMessage(
        asunto,
        mensaje,
        settings.DEFAULT_FROM_EMAIL,
        destinatarios
    )
    correo.send()


#Muestra un formulario para crear una inscripcion
def crear_inscripcion(request):
    if request.method == "POST":

        form = InscripcionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            inscripcion = form.save()
            enviar_correo_inscripcion(inscripcion)
            return redirect('lista_inscripciones')
    else:
        form = InscripcionForm()

    return render(request, 'crear_inscripcion.html', {'form': form})

# ###############################3
def cargar_grupos(request):

    curso_id = request.GET.get('curso')

    grupos = []

    for grupo in Grupo.objects.filter(curso_id=curso_id):

        ocupados = Inscripcion.objects.filter(
            grupo=grupo,
            estatus=EstatusInscripcion.ACTIVO
        ).count()

        disponibles = grupo.cupo - ocupados

        grupos.append({
            'id': grupo.id,
            'nombre': f'{grupo.nombre} ({disponibles} lugares disponibles)'
        })

    return JsonResponse(grupos, safe=False)

#Mustra el formulario con los datos registrados del la inscripcion
def editar_inscripcion(request, id):
    inscripcion = get_object_or_404(Inscripcion, pk=id)

    if request.method == "POST":
        form = InscripcionForm(
            request.POST,
            request.FILES,
            instance=inscripcion)

        if form.is_valid():
            form.save()
            return redirect('lista_inscripciones')

    else:
        form = InscripcionForm(instance=inscripcion)

    return render(request, 'editar_inscripcion.html', {'form': form,'inscripcion': inscripcion})

#Mustra una plantilla para confirmar la eliminacion
def eliminar_inscripcion(request, id):

    inscripcion = get_object_or_404(Inscripcion, pk=id)

    if request.method == 'POST':
        inscripcion.delete()
        return redirect('lista_inscripciones')

    return render(request, 'eliminar_inscripcion.html', {'inscripcion': inscripcion})


#CSRF error
#Cunado la sesion expiró
def csrf_failure(request, reason=""):
    return render(request, "csrf_error.html", {"reason": reason})
