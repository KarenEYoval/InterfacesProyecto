import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Voz_Asistente import VozAsistente

class LoginUI:
    def __init__(self, root, callback_login):
        self.root = root
        self.callback_login = callback_login

        root.title("Login")
        root.geometry("900x600")
        root.config(bg="#f4f4f4")

        self.estado_voz = "inicio"   # Para guiar los pasos del asistente

        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.construir_ui()

        # 🚀 ACTIVAR ASISTENTE AUTOMÁTICAMENTE AL INICIAR
        root.after(1000, self.iniciar_asistente_auto)

    def construir_ui(self):
        # COLUMNA IZQUIERDA
        izquierda = tk.Frame(self.frame, width=450, height=600)
        izquierda.pack(side="left", fill="both")

        img = Image.open("assets/login_bg.jpg")
        img = img.resize((450, 600))
        self.img_tk = ImageTk.PhotoImage(img)
        tk.Label(izquierda, image=self.img_tk).pack()

        # COLUMNA DERECHA
        derecha = tk.Frame(self.frame, bg="white")
        derecha.pack(side="right", fill="both", expand=True, padx=40)

        tk.Label(derecha, text="Inicio sesión",
                 font=("Arial", 26, "bold"), bg="white").pack(pady=40)

        # Usuario
        tk.Label(derecha, text="Usuario",
                 font=("Arial", 14), bg="white").pack(anchor="w")
        self.ent_usuario = ttk.Entry(derecha, width=40)
        self.ent_usuario.pack()

        # Contraseña
        tk.Label(derecha, text="Contraseña",
                 font=("Arial", 14), bg="white").pack(anchor="w", pady=(20,0))
        self.ent_contra = ttk.Entry(derecha, width=40, show="*")
        self.ent_contra.pack()

        # Botón ingresar (por si lo quieres usar manual)
        ttk.Button(derecha, text="Ingresar", command=self.login).pack(pady=40)

        # Texto del asistente
        self.label_transcripcion = tk.Label(derecha, text="",
                                            bg="white", fg="gray")
        self.label_transcripcion.pack()

        # Inicializar asistente
        self.asistente = VozAsistente(
            ui_callback_transcripcion=self.mostrar_transcripcion,
            ui_callback_comando=self.procesar_comando
        )

    # ----------- ASISTENTE AUTOMÁTICO -----------

    def iniciar_asistente_auto(self):
        self.estado_voz = "pedir_usuario"
        self.label_transcripcion.config(text="Bienvenido al login. Dime tu usuario.")
        self.asistente.activar()

    def mostrar_transcripcion(self, texto):
        self.label_transcripcion.config(text=f"Escuchando: {texto}")

    def procesar_comando(self, texto):
        texto = texto.lower()

        # 1️⃣ PEDIR USUARIO
        if self.estado_voz == "pedir_usuario":
            self.ent_usuario.delete(0, tk.END)
            self.ent_usuario.insert(0, texto)

            self.label_transcripcion.config(text="Perfecto. Ahora dime tu contraseña.")
            self.estado_voz = "pedir_contra"
            return

        # 2️⃣ PEDIR CONTRASEÑA
        if self.estado_voz == "pedir_contra":
            self.ent_contra.delete(0, tk.END)
            self.ent_contra.insert(0, texto)

            self.label_transcripcion.config(text="Ingresando...")
            self.estado_voz = "finalizar"
            self.login()
            return

    # ----------- LOGIN NORMAL -----------

    def login(self):
        usuario = self.ent_usuario.get()
        contra = self.ent_contra.get()

        rol = "estudiante"  # Simulado

        self.callback_login(usuario, rol)
