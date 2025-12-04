from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import qrcode
from reportlab.lib.utils import ImageReader
import os
from datetime import datetime


def generar_pdf(nombre_archivo, titulo, datos_alumno, tramite, materia):
    ruta = f"./{nombre_archivo}"

    c = canvas.Canvas(ruta, pagesize=letter)
    width, height = letter

    # ===========================
    # LOGO UV
    # ===========================
    logo_path = "assets/uv_logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 40, height - 120, width=90, height=90, mask='auto')

    # ===========================
    # ENCABEZADO
    # ===========================
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "Universidad Veracruzana")
    
    c.setFont("Helvetica", 13)
    c.drawCentredString(width / 2, height - 70, 
        "Facultad de Ingeniería y Ciencias de la Computación"
    )

    c.line(40, height - 140, width - 40, height - 140)

    # ===========================
    # TÍTULO DEL TRÁMITE
    # ===========================
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(width / 2, height - 170, titulo)

    # ===========================
    # DATOS DEL ALUMNO
    # ===========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 210, "Datos del alumno:")

    c.setFont("Helvetica", 12)
    c.drawString(60, height - 230, f"Nombre: {datos_alumno['nombre']}")
    c.drawString(60, height - 250, f"Matrícula: {datos_alumno['matricula']}")
    c.drawString(60, height - 270, f"Carrera: {datos_alumno['carrera']}")

    # ===========================
    # DETALLES DEL TRÁMITE
    # ===========================
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 310, "Detalles del trámite:")

    c.setFont("Helvetica", 12)
    c.drawString(60, height - 330, f"Tipo de trámite: {tramite}")
    c.drawString(60, height - 350, f"Materia: {materia}")

    # Fecha
    fecha = datetime.now().strftime("%d/%m/%Y  %I:%M %p")
    c.drawString(60, height - 370, f"Fecha de generación: {fecha}")

    # ===========================
    # GENERAR QR
    # ===========================
    qr_texto = f"{tramite} - {materia} - {datos_alumno['matricula']} - {fecha}"
    qr = qrcode.make(qr_texto)
    qr_path = "temp_qr.png"
    qr.save(qr_path)

    qr_img = ImageReader(qr_path)
    c.drawImage(qr_img, width - 170, height - 330, width=120, height=120)
    os.remove(qr_path)

    # ===========================
    # FIRMAS
    # ===========================
    y_firmas = 180

    c.setFont("Helvetica", 11)

    # Línea 1: Alumno
    c.line(60, y_firmas, width/2 - 40, y_firmas)
    c.drawString(60, y_firmas - 15, "Firma del Alumno(a)")

    # Línea 2: Docente
    c.line(width/2 + 40, y_firmas, width - 60, y_firmas)
    c.drawString(width/2 + 40, y_firmas - 15, "Docente / Responsable de la Experiencia Educativa")

    y_firmas -= 80

    # Línea 3: Jefe de carrera
    c.line(60, y_firmas, width/2 - 40, y_firmas)
    c.drawString(60, y_firmas - 15, "Jefe(a) de Carrera")

    # Línea 4: Director
    c.line(width/2 + 40, y_firmas, width - 60, y_firmas)
    c.drawString(width/2 + 40, y_firmas - 15, "Director(a) de Facultad")

    # ===========================
    # PIE DE PÁGINA
    # ===========================
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(
        width / 2, 
        40,
        "Este documento es un comprobante oficial de trámite generado automáticamente."
    )

    c.save()
    return ruta
