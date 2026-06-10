from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from datetime import date
from PIL import Image
import os

#Función para validar el formato en PDF
def validar_pdf(archivo):

    extension = os.path.splitext(
        archivo.name
    )[1].lower()

    if extension != '.pdf':
        raise ValidationError(
            'Solo se permiten archivos PDF.'
        )

#Función paara validar la foto del alumno
def validar_resolucion_imagen(imagen):
    img = Image.open(imagen)
    ancho, alto = img.size

    if ancho > 1920 or alto > 1080:
        raise ValidationError(
            "La imagen no puede superar 1920x1080 píxeles."
        )

    if imagen.size > 2 * 1024 * 1024:
        raise ValidationError(
        "La imagen no puede superar los 2 MB."
        )

#Validación para el número de télefono
telefono_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Debe contener exactamente 10 dígitos.'
)

#Clase para listar los tipos de contacto
class TipoContacto(models.TextChoices):
    SIN_CONTACTO = "", "Seleccionar"
    MOVIL = "Movil", "Móvil"
    FIJO = "Fijo", "Fijo"

#Clase para listar los tipos de sangre
class TipoSangre(models.TextChoices):
    A_POS = "A+", "A+"
    A_NEG = "A-", "A-"
    B_POS = "B+", "B+"
    B_NEG = "B-", "B-"
    AB_POS = "AB+", "AB+"
    AB_NEG = "AB-", "AB-"
    O_POS = "O+", "O+"
    O_NEG = "O-", "O-"

#Clase para listar los estatus del alumno
class EstatusAlumno(models.TextChoices):
    ACTIVO = "Activo", "Activo"
    INACTIVO = "Inactivo", "Inactivo"


#Clase para listar los estatus de inscripcion
class EstatusInscripcion(models.TextChoices):
    ACTIVO = "Activo", "Activo"
    INACTIVO = "Inactivo", "Inactivo"

#Clase para listar grados académicos
class GradoAcademico(models.TextChoices):
    PRIMARIA = "Primaria", "Primaria"
    SECUNDARIA = "Secundaria", "Secundaria"
    BACHILLERATO = "Bachillerato/Preparatoria", "Bachillerato/Preparatoria"
    TSU = "Tsu", "Técnico Superior Universitario"
    LICENCIATURA = "Licenciatura", "Licenciatura"
    INGENIERIA = "Ingenieria", "Ingeniería"

#Clase para listar los años escolares
class AñoEscolar(models.IntegerChoices):
    PRIMERO = 1, "1°"
    SEGUNDO = 2, "2°"
    TERCERO = 3, "3°"
    CUARTO = 4, "4°"
    QUINTO = 5, "5°"
    SEXTO = 6, "6°"
    SEPTIMO = 7, "7°"
    OCTAVO = 8, "8°"
    NOVENO = 9, "9°"
    DECIMO = 10, "10°"
    UNDECIMO = 11, "11°"

#Modelo/tabla para el registro de alumnos
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre(s)")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido materno")

    #calcula la edad apartir de la fecha de nacimiento
    @property
    def edad_calculada(self):
        hoy = date.today()

        return (
            hoy.year
            - self.fecha_nacimiento.year
            - (
                (hoy.month, hoy.day)
                <
                (self.fecha_nacimiento.month,
                 self.fecha_nacimiento.day)
            ))
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to='alumnos/', validators=[validar_resolucion_imagen], verbose_name="Fotografía")
    contacto_alumno = models.CharField(max_length=10, verbose_name="Numero telefónico", validators=[telefono_validator],)
    contacto_alumno_tipo = models.CharField(max_length=10, choices=TipoContacto.choices, verbose_name="Tipo de contacto")
    correo_electronico = models.EmailField()

    # Datos médicos
    alergias = models.BooleanField(default=False)
    alergias_detalle = models.CharField(max_length=200, blank=True)
    alergico_medicamento = models.BooleanField(default=False)
    alergico_medicamento_detalle = models.CharField(max_length=200, blank=True)
    tipo_sangre = models.CharField(max_length=3, choices=TipoSangre.choices, verbose_name="Tipo de sangre")

    # Datos de la madre
    madre_nombre = models.CharField(max_length=100, blank=True, verbose_name="Nombre(s)")
    madre_apellido_paterno = models.CharField(max_length=100, blank=True, verbose_name="Apellido paterno")
    madre_apellido_materno = models.CharField(max_length=100, blank=True, verbose_name="Apellido materno")
    madre_telefono = models.CharField(max_length=10, verbose_name="Número telefónico", blank=True, validators=[telefono_validator])
    madre_contacto_tipo = models.CharField(max_length=10, choices=TipoContacto.choices, blank=True, verbose_name="Tipo de contacto")
    madre_correo = models.EmailField(verbose_name="Correo electrónico", blank=True)

    # Datos del padre
    padre_nombre = models.CharField(max_length=100, blank=True, verbose_name="Nombre(s)")
    padre_apellido_paterno = models.CharField(max_length=100, blank=True, verbose_name="Apellido paterno")
    padre_apellido_materno = models.CharField(max_length=100, blank=True, verbose_name="Apellido materno")
    padre_telefono = models.CharField(max_length=10, verbose_name="Número telefónico", blank=True, validators=[telefono_validator])
    padre_contacto_tipo = models.CharField(max_length=10, choices=TipoContacto.choices, blank=True, verbose_name="Tipo de contacto")
    padre_correo = models.EmailField(verbose_name="Correo electrónico", blank=True)

    # Datos escolares
    escuela = models.CharField(max_length=150)
    grado = models.CharField(max_length=50, choices=GradoAcademico.choices, verbose_name="Nivel escolar")
    año = models.PositiveIntegerField(choices=AñoEscolar.choices, verbose_name="Año escolar")
    promedio_anterior = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Promedio del ciclo anterior",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ])
    # Datos de referencia
    persona_recoge = models.CharField(max_length=100, verbose_name="Persona que recoge")
    contacto_otro = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Numero telefónico",
        validators=[telefono_validator])
    contacto_otro_tipo = models.CharField(max_length=10, choices=TipoContacto.choices, verbose_name="Tipo de contacto")

    # Datos internos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    observaciones = models.TextField(max_length=150, blank=True)
    estatus = models.CharField(max_length=20, choices=EstatusAlumno.choices, default=EstatusAlumno.ACTIVO, verbose_name="Estatus")

    def clean(self):

        errores = {}

        if self.fecha_nacimiento and self.fecha_nacimiento > date.today():
            errores['fecha_nacimiento'] = (
            'La fecha de nacimiento no puede ser futura.'
        )

        if self.alergias and not self.alergias_detalle:
            errores['alergias_detalle'] = (
            'Debe indicar las alergias.'
        )

        if (
            self.alergico_medicamento and
            not self.alergico_medicamento_detalle
        ):
            errores['alergico_medicamento_detalle'] = (
                'Debe indicar el medicamento.'
            )

        if self.padre_nombre:
            if not self.padre_telefono:
                errores['padre_telefono'] = (
                    'Debe indicar un teléfono del padre.'
                )

        if self.madre_nombre:
            if not self.madre_telefono:
                errores['madre_telefono'] = (
                    'Debe indicar un teléfono de la madre.'
                )

        if errores:
            raise ValidationError(errores)


    def save(self, *args, **kwargs):
        # Validaciones: primera letra en mayúscula para todos los campos de texto
        campos_capitalize = [
            "nombre", 
            "apellido_paterno",
            "apellido_materno",
            "alergias_detalle", 
            "alergico_medicamento_detalle",
            "madre_nombre", 
            "madre_apellido_paterno", 
            "madre_apellido_materno",
            "padre_nombre", 
            "padre_apellido_paterno", 
            "padre_apellido_materno",
            "escuela",
            "persona_recoge",
        ]

        for campo in campos_capitalize:
            valor = getattr(self, campo)
            if valor and valor != "null":
                setattr(self, campo, " ".join([w.capitalize() for w in valor.split()]))
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"


############################################
#Modelo/tabla para el registro de Cursos
class Curso(models.Model):
    nombre = models.CharField(max_length=150, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre


###########################################
#Modelo/tabla para el registro de Grupos
class Grupo(models.Model):

    nombre = models.CharField(max_length=50)

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    horario = models.CharField(max_length=50)

    cupo = models.PositiveIntegerField(default=20, verbose_name="Tamaño del grupo (cupo)")

    #def clean(self):
        #validaciones
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


############################################
#Modelo/tabla para el registro de inscripciones
class Inscripcion(models.Model):

    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')

    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)

    fecha_inscripcion = models.DateField(verbose_name="Fecha de inscripción")

    contrato_firmado = models.BooleanField(
        default=False,
        verbose_name="Contrato firmado"
    )

    contrato_pdf = models.FileField(
        upload_to='contratos/',
        validators=[validar_pdf],
        blank=True,
        null=True,
        verbose_name="Contrato (PDF)"
    )

    estatus = models.CharField(max_length=15, choices=EstatusInscripcion.choices, default=EstatusInscripcion.ACTIVO)

    fecha_baja = models.DateField(blank=True, null=True, verbose_name="Fecha de finalización")

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    fecha_actualizacion = models.DateTimeField(auto_now=True)

    observaciones = models.TextField(blank=True)

    def clean(self):

        errores = {}

        if self.contrato_firmado and not self.contrato_pdf:
            errores['contrato_pdf'] = ('Debe adjuntar el contrato en PDF.')

        if not self.contrato_firmado and self.contrato_pdf:
            errores['contrato_firmado'] = ('Debe marcar la casilla de contrato.')

        if (self.fecha_baja and self.fecha_baja <= self.fecha_inscripcion):
            errores['fecha_baja'] = (
                'La fecha de finalización debe ser posterior a la fecha de inscripción.')

        # Validar cupo del grupo
        if self.grupo:
            #Solo cuenta los alumnos activos
            inscritos = Inscripcion.objects.filter(
                grupo=self.grupo,
                estatus=EstatusInscripcion.ACTIVO
            )

            # Si se está editando una inscripción,
            # excluir el registro actual
            if self.pk:
                inscritos = inscritos.exclude(pk=self.pk)

            if inscritos.count() >= self.grupo.cupo:
                errores['grupo'] = (
                    f'El grupo "{self.grupo}" ya alcanzó su cupo máximo '
                    f'({self.grupo.cupo} alumnos).')

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.alumno} - {self.grupo}"

    class Meta:
        constraints = [models.UniqueConstraint(fields=['alumno', 'grupo'], name='inscripcion_unica')]


