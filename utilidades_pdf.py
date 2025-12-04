from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

def generar_pdf(nombre_archivo, titulo, datos_alumno, tramite, materia=None):
    # Crear carpeta de salida si no existe
    if not os.path.exists("pdf_tramites"):
        os.makedirs("pdf_tramites")

    ruta = os.path.join("pdf_tramites", nombre_archivo)

    c = canvas.Canvas(ruta, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, titulo)

    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y - %H:%M')}")

    # Datos del alumno
    c.drawString(50, 690, "-----------------------------------------")
    c.drawString(50, 675, "DATOS DEL ALUMNO")
    c.drawString(50, 660, "-----------------------------------------")

    c.drawString(50, 640, f"Nombre: {datos_alumno['nombre']}")
    c.drawString(50, 625, f"Matrícula: {datos_alumno['matricula']}")
    c.drawString(50, 610, f"Carrera: {datos_alumno['carrera']}")

    # Trámite
    c.drawString(50, 580, "-----------------------------------------")
    c.drawString(50, 565, "TRÁMITE REALIZADO")
    c.drawString(50, 550, "-----------------------------------------")

    c.drawString(50, 530, f"Trámite: {tramite}")

    if materia:
        c.drawString(50, 510, f"Materia: {materia}")

    c.drawString(50, 480, "El trámite ha sido registrado correctamente.")
    c.drawString(50, 460, "Gracias por utilizar el sistema.")

    c.save()

    return ruta
