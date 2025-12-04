import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Voz_Asistente import VozAsistente


class LoginUI:
    def __init__(self, root, callback_login):
        self.root = root
        self.callback_login = callback_login

        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.construir_ui()

        # activar el asistente 1 segundo después
        root.after(1000, self.iniciar_asistente)

    def construir_ui(self):
        izquierda = tk.Frame(self.frame, width=450, height=600)
        izquierda.pack(side="left", fill="both")

        img = Image.open("assets/login_bg.jpg")
        img = img.resize((450, 600))
        self.img = ImageTk.PhotoImage(img)
        tk.Label(izquierda, image=self.img).pack()

        derecha = tk.Frame(self.frame, bg="white")
        derecha.pack(side="right", fill="both", expand=True, padx=40)

        tk.Label(derecha, text="Inicio de sesión",
                 font=("Arial", 26, "bold"), bg="white").pack(pady=40)

        tk.Label(derecha, text="Usuario",
                 font=("Arial", 14), bg="white").pack(anchor="w")
        self.ent_usuario = ttk.Entry(derecha, width=40)
        self.ent_usuario.pack()

        tk.Label(derecha, text="Contraseña",
                 font=("Arial", 14), bg="white").pack(anchor="w", pady=(20, 0))
        self.ent_contra = ttk.Entry(derecha, width=40, show="*")
        self.ent_contra.pack()

        ttk.Button(derecha, text="Ingresar",
                   command=self.login_manual).pack(pady=40)

        self.label_transcripcion = tk.Label(
            derecha, text="", fg="gray", bg="white")
        self.label_transcripcion.pack()

        # instancia del asistente
        self.asistente = VozAsistente(
            ui_callback_transcripcion=self.mostrar,
            ui_callback_comando=self.procesar
        )

        # 🔥 ESTA LÍNEA DEBE ESTAR DENTRO DE __init__
        self.root.asistente = self.asistente

    # ACTIVAR ASISTENTE
    def iniciar_asistente(self):
        mensaje = (
            "Bienvenido al login. "
            "Dime tu usuario y contraseña juntos Por ejemplo: Karen uno dos tres."
        )
        self.label_transcripcion.config(text=mensaje)
        self.asistente.hablar(mensaje)
        self.asistente.activar()

    def mostrar(self, texto):
        self.label_transcripcion.config(text=f"Escuchando: {texto}")

    # PROCESAR COMANDO DE UNA VEZ
    def procesar(self, texto):
        partes = texto.split()

        if len(partes) < 2:
            self.asistente.hablar("Por favor di usuario y contraseña juntos.")
            return

        usuario = partes[0]
        contrasena = " ".join(partes[1:])

        # llenar campos
        self.ent_usuario.delete(0, tk.END)
        self.ent_usuario.insert(0, usuario)

        self.ent_contra.delete(0, tk.END)
        self.ent_contra.insert(0, contrasena)

        # confirmación
        self.asistente.hablar("Datos recibidos. Ingresando ahora.")

        # pasar a trámites
        self.root.after(1500, lambda: self.callback_login(
            usuario, "estudiante"))

    def login_manual(self):
        usuario = self.ent_usuario.get()
        self.callback_login(usuario, "estudiante")
