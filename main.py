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

    # Puedes agregar más pantallas si quieres aquí:
    # if destino == "estado": ...
    # if destino == "historial": ...

    if destino == "inicio":
        # Volver al login
        for widget in root.winfo_children():
            widget.destroy()
        LoginUI(root, mostrar_pantalla_tramites)


# ----------------------------------------------
# ESTA FUNCIÓN RECIBE usuario Y rol DESDE LoginUI
# ----------------------------------------------
def mostrar_pantalla_tramites(usuario, rol):
    print("Login exitoso:", usuario, rol)

    # LIMPIAR LOGIN
    for widget in root.winfo_children():
        widget.destroy()

    # CREAR PANTALLA DE TRÁMITES
    TramitesUI(root, callback_navegar=navegar_tramites)


# ----------------------------------------------
# MOSTRAR LOGIN
# ----------------------------------------------
LoginUI(root, callback_login=mostrar_pantalla_tramites)

root.mainloop()
