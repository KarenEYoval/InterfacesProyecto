import tkinter as tk

from ui_login import LoginUI
from ui_tramites import TramitesUI
from ui_solicitud import SolicitudUI
from ui_baja import BajaMateriaUI
from ui_extraordinario import ExtraordinarioUI
from ui_titulo import TituloUI


# ---------------------------------------------------
#     INICIALIZAR APLICACIÓN
# ---------------------------------------------------
root = tk.Tk()
root.title("Sistema de Trámites Escolares")
root.geometry("1200x720")
root.minsize(1200, 720)


# ---------------------------------------------------
#     NAVEGACIÓN ENTRE PANTALLAS
# ---------------------------------------------------
def navegar(destino, datos_usuario=None):

    # limpiar ventana actual
    for widget in root.winfo_children():
        widget.destroy()

    # -------- LOGIN ------------
    if destino == "login":
        LoginUI(root, callback_login=mostrar_tramites)

    # -------- TRÁMITES ---------
    elif destino == "tramites":
        TramitesUI(root, navegar, datos_usuario)

    # -------- ALTA DE MATERIA ---------
    elif destino == "Alta de experiencia educativa":
        SolicitudUI(root, datos_usuario)

    # -------- BAJA DE MATERIA ---------
    elif destino == "Baja de experiencia educativa":
        BajaMateriaUI(root, datos_usuario)

    # -------- EXTRAORDINARIO ---------
    elif destino == "Examen extraordinario":
        ExtraordinarioUI(root, datos_usuario)

    # -------- TÍTULO DE SUFICIENCIA ---------
    elif destino == "Título de suficiencia":
        TituloUI(root, datos_usuario)

    else:
        print("⚠ Trámite desconocido:", destino)


# ---------------------------------------------------
#      LOGIN → TRÁMITES
# ---------------------------------------------------
def mostrar_tramites(datos_usuario, rol):

    # detener asistente del login
    if hasattr(root, "asistente"):
        try:
            root.asistente.detener()
        except:
            pass

    navegar("tramites", datos_usuario)


# ---------------------------------------------------
#      INICIAR PRIMERA PANTALLA (LOGIN)
# ---------------------------------------------------
LoginUI(root, callback_login=mostrar_tramites)

root.mainloop()
