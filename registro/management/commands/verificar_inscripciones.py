from django.core.management.base import BaseCommand
from datetime import date

from registro.models import Inscripcion, EstatusInscripcion
from registro.services.correos import enviar_correo_fin_inscripcion


class Command(BaseCommand):
    help = "Verifica inscripciones vencidas"

    def handle(self, *args, **kwargs):

        inscripciones = Inscripcion.objects.filter(
            fecha_baja__isnull=False,
            fecha_baja__lte=date.today(),
            estatus=EstatusInscripcion.ACTIVO
        )

        for inscripcion in inscripciones:
            inscripcion.estatus = EstatusInscripcion.INACTIVO
            inscripcion.save()

            enviar_correo_fin_inscripcion(inscripcion)

        self.stdout.write(
            self.style.SUCCESS(
                f"{inscripciones.count()} inscripciones verificadas"
            )
        )