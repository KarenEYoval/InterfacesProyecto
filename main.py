import tkinter as tk
from ui_login import LoginUI
from ui_tramites import TramitesUI


root = tk.Tk()
root.title("Sistema de Trámites")


# ----------------------------------------------
# NAVEGACIÓN DESDE TRÁMITES
# ----------------------------------------------
def navegar_tramites(destino):
    print("Destino solicitado:", destino)

    if destino == "inicio":
        # Volver al login
        for widget in root.winfo_children():
            widget.destroy()
        LoginUI(root, callback_login=mostrar_pantalla_tramites)


# ----------------------------------------------
# ESTO SE EJECUTA DESPUÉS DEL LOGIN
# ----------------------------------------------
def mostrar_pantalla_tramites(usuario, rol):

    # detener escucha del login
    if hasattr(root, "asistente"):
        root.asistente.detener()

    for widget in root.winfo_children():
        widget.destroy()

    # ✔ AGREGAR LA NAVEGACIÓN CORRECTA
    TramitesUI(root, navegar_tramites)


# ----------------------------------------------
# MOSTRAR LOGIN
# ----------------------------------------------
LoginUI(root, callback_login=mostrar_pantalla_tramites)

root.mainloop()
