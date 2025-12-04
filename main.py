import tkinter as tk
from ui_login import LoginUI
from ui_tramites import TramitesUI
from ui_solicitud import SolicitudUI   # ← importar nueva pantalla


root = tk.Tk()
root.title("Sistema de Trámites")

def centrar_ventana(root, ancho=500, alto=500):
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (ancho // 2)
    y = (root.winfo_screenheight() // 2) - (alto // 2)
    root.geometry(f"{ancho}x{alto}+{x}+{y}")

    
    root.geometry("1200x720")
    root.minsize(1200, 720)


# ----------------------------------------------
# NAVEGACIÓN ENTRE PANTALLAS
# ----------------------------------------------
def navegar(destino, datos=None):

    # limpiar pantalla
    for widget in root.winfo_children():
        widget.destroy()

    if destino == "tramites":
        TramitesUI(root, navegar, datos)

    elif destino == "solicitud":
        SolicitudUI(root, datos)

    elif destino == "inicio":
        LoginUI(root, callback_login=mostrar_pantalla_tramites)


# ----------------------------------------------
# LOGIN → TRÁMITES
# ----------------------------------------------
def mostrar_pantalla_tramites(datos_usuario, rol):
    # detener asistente del login
    if hasattr(root, "asistente"):
        root.asistente.detener()

    navegar("tramites", datos_usuario)


# ----------------------------------------------
# INICIAR LOGIN
# ----------------------------------------------
LoginUI(root, callback_login=mostrar_pantalla_tramites)

root.mainloop()
