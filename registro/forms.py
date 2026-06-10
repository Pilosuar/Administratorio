from django import forms
from .models import Alumno, Curso, Grupo, Inscripcion

class AlumnoForm(forms.ModelForm):

    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fecha_nacimiento'].input_formats = ['%Y-%m-%d']

        for nombre, campo in self.fields.items():

            if isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs['class'] = 'form-check-input'
            else:
                campo.widget.attrs['class'] = 'form-control'

        if self.errors:
            for campo in self.errors:
                if campo in self.fields:
                    clase_actual = self.fields[campo].widget.attrs.get(
                        'class', ''
                    )
                    self.fields[campo].widget.attrs['class'] = (
                        clase_actual + ' is-invalid'
                    )

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')

        # Si es edición y ya existe una foto, no obligar a subir otra
        if not foto and self.instance.pk and self.instance.foto:
            return self.instance.foto

        if not foto:
            raise forms.ValidationError(
                "Debe seleccionar una fotografía del alumno."
            )

        extensiones = ['jpg', 'jpeg', 'png']

        extension = foto.name.split('.')[-1].lower()

        if extension not in extensiones:
            raise forms.ValidationError(
                "Solo se permiten imágenes JPG o PNG."
            )

        return foto

    def clean(self):
        cleaned_data = super().clean()

        for nombre, campo in self.fields.items():

            valor = cleaned_data.get(nombre)

            if campo.required:

                if valor is None:
                    self.add_error(
                        nombre,
                        "Este campo es obligatorio."
                    )

                elif isinstance(valor, str) and not valor.strip():
                    self.add_error(
                        nombre,
                        "Este campo no puede estar vacío."
                    )

        return cleaned_data


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InscripcionForm(forms.ModelForm):
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all(),
        required=True,
        label="Curso"
    )

    class Meta:
        model = Inscripcion
        fields = [
            'alumno',
            'curso',
            'grupo',
            'fecha_inscripcion',
            'contrato_firmado',
            'contrato_pdf',
            'estatus',
            'fecha_baja',
            'observaciones',
        ]

        widgets = {
            'fecha_inscripcion': forms.DateInput(
                attrs={'type': 'date'},  format='%Y-%m-%d'
            ),
            'fecha_baja': forms.DateInput(
                attrs={'type': 'date'},  format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['grupo'].queryset = Grupo.objects.none()

        if 'curso' in self.data:
            try:
                curso_id = int(self.data.get('curso'))
                self.fields['grupo'].queryset = Grupo.objects.filter(
                    curso_id=curso_id
                )
            except (ValueError, TypeError):
                pass



