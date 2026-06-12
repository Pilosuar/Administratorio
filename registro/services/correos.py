from django.conf import settings
from django.core.mail import EmailMessage
import os


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

