from django.urls import path, include
from registro import views
from registro import exportaciones

urlpatterns = [
    path('', views.plantilla, name='plantilla'),
    path('error/', views.csrf_failure, name="error_csrf"),
    # ==========================
    # ALUMNOS
    # ==========================
    path('alumnos/', views.lista_alumnos, name='lista_alumnos'),
    path('alumnos/nuevo/', views.crear_alumno, name='crear_alumno'),
    path('alumnos/<int:pk>/', views.detalle_alumno, name='detalle_alumno'),
    path('alumnos/<int:pk>/editar/', views.editar_alumno, name='editar_alumno'),
    path('alumnos/<int:pk>/eliminar/', views.eliminar_alumno, name='eliminar_alumno'),
    # ==========================
    # CURSOS
    # ==========================
    path('cursos/', views.lista_cursos, name='lista_cursos'),
    path('cursos/nuevo/', views.crear_curso, name='crear_curso'),
    path('cursos/<int:id>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:id>/eliminar/', views.eliminar_curso, name='eliminar_curso'),
    # ==========================
    # GRUPOS
    # ==========================
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/nuevo/', views.crear_grupo, name='crear_grupo'),
    path('grupos/<int:id>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupos/<int:id>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),
    # ==========================
    # INSCRIPCIONES
    # ==========================
    path('inscripciones/', views.lista_inscripciones, name='lista_inscripciones'),
    path('inscripciones/nueva/', views.crear_inscripcion, name='crear_inscripcion'),
    path('ajax/cargar-grupos/', views.cargar_grupos, name='ajax_cargar_grupos'),
    path('inscripciones/<int:id>/editar/', views.editar_inscripcion, name='editar_inscripcion'),
    path('inscripciones/<int:id>/eliminar/', views.eliminar_inscripcion, name='eliminar_inscripcion'),

    # ==========================
    # EXPORTACIONES
    # ==========================
    path('alumnos/excel/', exportaciones.exportar_alumnos_excel, name='exportar_alumnos_excel'),
    path("alumno/pdf/<int:id_alumno>/", exportaciones.descargar_pdf_alumno, name="descargar_pdf_alumno"),
    path('inscripciones/excel/', exportaciones.exportar_inscripciones_excel, name='exportar_inscripciones_excel'),
    path('cursos/excel/', exportaciones.exportar_cursos_excel, name='exportar_cursos_excel'),
    path('cursos/<int:id>/reporte/', exportaciones.exportar_curso_excel, name='exportar_curso_excel'),
    path('grupos/excel/', exportaciones.exportar_grupos_excel, name='exportar_grupos_excel'),

]