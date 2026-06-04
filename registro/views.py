from django.shortcuts import render, redirect
from .models import Alumno
from .forms import AlumnoForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import (
    Alumno,
    Curso,
    Grupo,
    Inscripcion
)

from .forms import (
    AlumnoForm,
    CursoForm,
    GrupoForm,
    InscripcionForm
)

def plantilla(request):
    return render(request, "plantilla.html")
    
### ALUMNOS
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()

    return render(request, 'alumno_form.html', {
        'form': form
    })

def lista_alumnos(request):

    buscar = request.GET.get('buscar', '')

    alumnos = Alumno.objects.prefetch_related(
        'inscripciones__grupo__curso'
    ).order_by('apellido_paterno', 'apellido_materno', 'nombre')

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

    return render(
        request,
        'registro/lista_alumnos.html',
        {
            'page_obj': page_obj,
            'buscar': buscar
        }
    )

def detalle_alumno(request, pk):

    alumno = get_object_or_404(
        Alumno,
        pk=pk
    )

    return render(
        request,
        'registro/detalle_alumno.html',
        {
            'alumno': alumno
        }
    )

def editar_alumno(request, pk):

    alumno = get_object_or_404(
        Alumno,
        pk=pk
    )

    if request.method == 'POST':

        form = AlumnoForm(
            request.POST,
            request.FILES,
            instance=alumno
        )

        if form.is_valid():

            form.save()

            return redirect('lista_alumnos')

    else:

        form = AlumnoForm(
            instance=alumno
        )

    return render(
        request,
        'editar_alumno.html',
        {
            'form': form
        }
    )

def eliminar_alumno(request, pk):

    alumno = get_object_or_404(
        Alumno,
        pk=pk
    )

    if request.method == 'POST':

        alumno.delete()

        return redirect(
            'lista_alumnos'
        )

    return render(
        request,
        'eliminar_alumno.html',
        {
            'alumno': alumno
        }
    )

### CURSOS
def lista_cursos(request):

    cursos = Curso.objects.all()

    return render(
        request,
        'lista_cursos.html',
        {'cursos': cursos}
    )

def crear_curso(request):

    if request.method == 'POST':

        form = CursoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_cursos')

    else:
        form = CursoForm()

    return render(
        request,
        'crear_curso.html',
        {'form': form}
    )

def editar_curso(request, id):

    curso = get_object_or_404(
        Curso,
        pk=id
    )

    if request.method == 'POST':

        form = CursoForm(
            request.POST,
            instance=curso
        )

        if form.is_valid():
            form.save()
            return redirect('lista_cursos')

    else:
        form = CursoForm(
            instance=curso
        )

    return render(
        request,
        'editar_curso.html',
        {
            'form': form,
            'curso': curso
        }
    )

def eliminar_curso(request, id):

    curso = get_object_or_404(
        Curso,
        pk=id
    )

    if request.method == 'POST':
        curso.delete()
        return redirect('lista_cursos')

    return render(
        request,
        'eliminar_curso.html',
        {'curso': curso}
    )

### GRUPOS

def lista_grupos(request):

    grupos = Grupo.objects.all()

    return render(
        request,
        'lista_grupos.html',
        {'grupos': grupos}
    )

def crear_grupo(request):

    if request.method == 'POST':

        form = GrupoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_grupos')

    else:
        form = GrupoForm()

    return render(
        request,
        'crear_grupo.html',
        {'form': form}
    )

def editar_grupo(request, id):

    grupo = get_object_or_404(
        Grupo,
        pk=id
    )

    if request.method == 'POST':

        form = GrupoForm(
            request.POST,
            instance=grupo
        )

        if form.is_valid():
            form.save()
            return redirect('lista_grupos')

    else:
        form = GrupoForm(
            instance=grupo
        )

    return render(
        request,
        'editar_grupo.html',
        {
            'form': form,
            'grupo': grupo
        }
    )

def eliminar_grupo(request, id):

    grupo = get_object_or_404(
        Grupo,
        pk=id
    )

    if request.method == 'POST':
        grupo.delete()
        return redirect('lista_grupos')

    return render(
        request,
        'eliminar_grupo.html',
        {'grupo': grupo}
    )

### INSCRIPCIONES
def lista_inscripciones(request):

    inscripciones = (
        Inscripcion.objects
        .select_related(
            'alumno',
            'grupo',
            'grupo__curso'
        )
    )

    return render(
        request,
        'lista_inscripciones.html',
        {
            'inscripciones': inscripciones
        }
    )

def crear_inscripcion(request):

    if request.method == 'POST':

        form = InscripcionForm(
            request.POST
        )

        if form.is_valid():
            form.save()
            return redirect(
                'lista_inscripciones'
            )

    else:
        form = InscripcionForm()

    return render(
        request,
        'crear_inscripcion.html',
        {'form': form}
    )

def editar_inscripcion(request, id):

    inscripcion = get_object_or_404(
        Inscripcion,
        pk=id
    )

    if request.method == 'POST':

        form = InscripcionForm(
            request.POST,
            instance=inscripcion
        )

        if form.is_valid():
            form.save()
            return redirect(
                'lista_inscripciones'
            )

    else:
        form = InscripcionForm(
            instance=inscripcion
        )

    return render(
        request,
        'editar_inscripcion.html',
        {
            'form': form,
            'inscripcion': inscripcion
        }
    )

def eliminar_inscripcion(request, id):

    inscripcion = get_object_or_404(
        Inscripcion,
        pk=id
    )

    if request.method == 'POST':
        inscripcion.delete()
        return redirect(
            'lista_inscripciones'
        )

    return render(
        request,
        'eliminar_inscripcion.html',
        {
            'inscripcion': inscripcion
        }
    )


#CSRF error
def csrf_failure(request, reason=""):
    return render(request, "csrf_error.html", {"reason": reason})
