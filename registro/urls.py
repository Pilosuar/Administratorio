from django.urls import path, include
from registro import views

urlpatterns = [
    path('error/', views.csrf_failure, name="error_csrf"),
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alumnos/nuevo/', views.crear_alumno, name='crear_alumno'),
    path('alumnos/<int:pk>/', views.detalle_alumno, name='detalle_alumno'),
    path('alumnos/<int:pk>/editar/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/<int:pk>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
]