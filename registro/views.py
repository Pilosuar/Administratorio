from django.shortcuts import render, redirect
from .models import Alumno
from .forms import AlumnoForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404


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

    alumnos = Alumno.objects.all()

    if buscar:
        alumnos = alumnos.filter(
            Q(nombre__icontains=buscar) |
            Q(apellido_paterno__icontains=buscar) |
            Q(apellido_materno__icontains=buscar) |
            Q(escuela__icontains=buscar) |
            Q(curso__icontains=buscar)
        )

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
        'registro/eliminar_alumno.html',
        {
            'alumno': alumno
        }
    )

#CSRF error
def csrf_failure(request, reason=""):
    return render(request, "csrf_error.html", {"reason": reason})
