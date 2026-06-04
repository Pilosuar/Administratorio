from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator
from datetime import date
from PIL import Image

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

telefono_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='Debe contener exactamente 10 dígitos.'
)

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre(s)")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido materno")
    estado = models.CharField(max_length=50)
    edad = models.PositiveIntegerField(
    validators=[
        MinValueValidator(1, message="La edad debe ser mayor a 0."), 
        MaxValueValidator(100, message="La edad no puede ser mayor a 100.")]
    )
    fecha_nacimiento = models.DateField()

    foto = models.ImageField(upload_to='alumnos/', validators=[validar_resolucion_imagen], verbose_name="Fotografía")

    contacto_alumno = models.CharField(max_length=10, verbose_name="Numero telefónico", validators=[telefono_validator],)
    TIPOS_CONTACTO = [
    ('', 'Seleccionar un tipo'),
    ('Movil', 'Móvil'),
    ('Fijo', 'Fijo'),
    ]
    contacto_alumno_tipo = models.CharField(max_length=10, choices=TIPOS_CONTACTO, verbose_name="Tipo de contacto")
    correo_electronico = models.EmailField()

    # Datos médicos
    alergias = models.BooleanField(default=False)
    alergias_detalle = models.CharField(max_length=200, blank=True)
    alergico_medicamento = models.BooleanField(default=False)
    alergico_medicamento_detalle = models.CharField(max_length=200, blank=True)
    TIPOS_SANGRE = [
    ('', 'Seleccionar'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ]

    tipo_sangre = models.CharField(max_length=3, choices=TIPOS_SANGRE, verbose_name="Tipo de sangre")
    # Datos de la madre
    madre_nombre = models.CharField(max_length=100, blank=True, verbose_name="Nombre(s)")
    madre_apellido_paterno = models.CharField(max_length=100, blank=True, verbose_name="Apellido paterno")
    madre_apellido_materno = models.CharField(max_length=100, blank=True, verbose_name="Apellido materno")
    madre_telefono = models.CharField(max_length=10, verbose_name="Número telefónico", blank=True, validators=[telefono_validator])
    madre_contacto_tipo = models.CharField(max_length=10, choices=TIPOS_CONTACTO, verbose_name="Tipo de contacto")

    madre_correo = models.EmailField(verbose_name="Correo electrónico", blank=True)

    # Datos del padre
    padre_nombre = models.CharField(max_length=100, blank=True, verbose_name="Nombre(s)")
    padre_apellido_paterno = models.CharField(max_length=100, blank=True, verbose_name="Apellido paterno")
    padre_apellido_materno = models.CharField(max_length=100, blank=True, verbose_name="Apellido materno")
    padre_telefono = models.CharField(max_length=10, verbose_name="Número telefónico", blank=True, validators=[telefono_validator])
    padre_contacto_tipo = models.CharField(max_length=10, choices=TIPOS_CONTACTO, blank=True, verbose_name="Tipo de contacto")
    padre_correo = models.EmailField(verbose_name="Correo electrónico", blank=True)

    # Datos escolares
    escuela = models.CharField(max_length=150)
    grado = models.CharField(max_length=50, verbose_name="Nivel escolar")
    año = models.PositiveIntegerField()
    promedio_anterior = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="Promedio del ciclo anterior",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    # Datos de referencia
    persona_recoge = models.CharField(max_length=100, verbose_name="Persona que recoge")
    contacto_padre = models.CharField(
        max_length=10,
        verbose_name="Numero telefónico",
        validators=[telefono_validator]
    )
    contacto_padre_tipo = models.CharField(max_length=10, choices=TIPOS_CONTACTO, verbose_name="Tipo de contacto")

    # Datos internos
    fecha_inscripcion = models.DateField(verbose_name="fecha de inscirpcion")
    curso = models.CharField(max_length=150)
    horario = models.CharField(max_length=50)
    contrato = models.CharField(max_length=50)
    observaciones = models.TextField(max_length=150, blank=True)

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

        if errores:
            raise ValidationError(errores)


    def save(self, *args, **kwargs):
        # Validaciones: primera letra en mayúscula para todos los campos de texto
        campos_capitalize = [
            "nombre", 
            "apellido_paterno",
            "apellido_materno", 
            "estado",
            "alergias_detalle", 
            "alergico_medicamento_detalle",
            "madre_nombre", 
            "madre_apellido_paterno", 
            "madre_apellido_materno",
            "padre_nombre", 
            "padre_apellido_paterno", 
            "padre_apellido_materno",
            "escuela", 
            "grado", 
            "persona_recoge", 
            "contacto_padre_tipo",
            "contacto_alumno_tipo", 
            "curso", 
            "horario", 
            "contrato"
        ]

        for campo in campos_capitalize:
            valor = getattr(self, campo)
            if valor and valor != "null":
                setattr(self, campo, " ".join([w.capitalize() for w in valor.split()]))
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
