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

        # Estado del flujo de voz
        self.estado_voz = "inicio"

        # Para recordar lo que dijo el usuario
        self.usuario_voz = ""
        self.contra_voz = ""

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

        tk.Label(
            derecha,
            text="Inicio sesión",
            font=("Arial", 26, "bold"),
            bg="white"
        ).pack(pady=40)

        # Usuario
        tk.Label(
            derecha,
            text="Usuario",
            font=("Arial", 14),
            bg="white"
        ).pack(anchor="w")
        self.ent_usuario = ttk.Entry(derecha, width=40)
        self.ent_usuario.pack()

        # Contraseña
        tk.Label(
            derecha,
            text="Contraseña",
            font=("Arial", 14),
            bg="white"
        ).pack(anchor="w", pady=(20, 0))
        self.ent_contra = ttk.Entry(derecha, width=40, show="*")
        self.ent_contra.pack()

        # Botón ingresar manual
        ttk.Button(derecha, text="Ingresar", command=self.login).pack(pady=40)

        # Texto del asistente
        self.label_transcripcion = tk.Label(
            derecha,
            text="",
            bg="white",
            fg="gray"
        )
        self.label_transcripcion.pack()

        # Inicializar asistente de voz
        self.asistente = VozAsistente(
            ui_callback_transcripcion=self.mostrar_transcripcion,
            ui_callback_comando=self.procesar_comando
        )

    # ----------- ASISTENTE AUTOMÁTICO -----------

    def iniciar_asistente_auto(self):
        self.estado_voz = "pedir_usuario"
        mensaje = "Bienvenido al login. Dime tu usuario."
        self.label_transcripcion.config(text=mensaje)
        self.asistente.hablar(mensaje)
        self.asistente.activar()  # primera escucha

    def mostrar_transcripcion(self, texto):
        self.label_transcripcion.config(text=f"Escuchando: {texto}")

    # ----------- MANEJO DE COMANDOS DE VOZ -----------

    def procesar_comando(self, texto):
        print("DEBUG procesar_comando -> estado:", self.estado_voz, "| texto:", texto)
        texto = texto.strip()

        # 1️⃣ PEDIR USUARIO
        if self.estado_voz == "pedir_usuario":
            # Guardamos lo que dijo como usuario
            self.usuario_voz = texto

            # Lo ponemos en el campo de usuario
            self.ent_usuario.delete(0, tk.END)
            self.ent_usuario.insert(0, self.usuario_voz)

            mensaje = (
                f"Perfecto. De usuario dijiste: {self.usuario_voz}. "
                f"Ahora dime tu contraseña."
            )
            self.label_transcripcion.config(text=mensaje)
            self.asistente.hablar(mensaje)

            # Pasamos a pedir contraseña
            self.estado_voz = "pedir_contra"

            # Volver a escuchar después de hablar
            self.root.after(1000, self.asistente.activar)
            return

        # 2️⃣ PEDIR CONTRASEÑA
        if self.estado_voz == "pedir_contra":
            # Guardamos lo que dijo como contraseña
            self.contra_voz = texto

            # Lo ponemos en el campo de contraseña
            self.ent_contra.delete(0, tk.END)
            self.ent_contra.insert(0, self.contra_voz)

            # 👉 Aquí repite usuario Y contraseña
            mensaje = (
                f"Perfecto. De usuario dijiste: {self.usuario_voz}. "
                f"De contraseña dijiste: {self.contra_voz}. "
                f"Ingresando ahora."
            )
            self.label_transcripcion.config(text=mensaje)
            self.asistente.hablar(mensaje)

            self.estado_voz = "finalizar"
            self.login()
            return

        # Cualquier otro estado inesperado
        self.label_transcripcion.config(text=f"No esperaba esto: {texto}")

    # ----------- LOGIN NORMAL -----------

    def login(self):
        usuario = self.ent_usuario.get()
        contra = self.ent_contra.get()

        rol = "estudiante"  # Simulado

        self.callback_login(usuario, rol)
