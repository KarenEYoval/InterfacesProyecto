import tkinter as tk
from ui_login import LoginUI
from ui_tramites import TramitesUI

# Función para cambiar de pantalla
def mostrar_pantalla_tramites(rol):
    # Cerrar pantalla anterior
    for widget in root.winfo_children():
        widget.destroy()

    TramitesUI(root, rol)

root = tk.Tk()
root.title("Sistema de Trámites")

# Inicializar pantalla de login
LoginUI(root, mostrar_pantalla_tramites)

root.mainloop()
