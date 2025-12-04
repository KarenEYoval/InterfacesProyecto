import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Voz_Asistente import VozAsistente
from base_datos import usuarios
from utilidades import centrar_ventana


class LoginUI:
    def __init__(self, root, callback_login):
        self.root = root
        self.callback_login = callback_login

        # Centrar ventana a tamaño ideal
        centrar_ventana(root, 850, 600)

        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.asistente = None  # Se creará más adelante

        self.construir_ui()

        # Guardamos el asistente para reuso en otras pantallas
        self.root.asistente = self.asistente

        # Activar asistente 1 s después
        root.after(1000, self.iniciar_asistente)

    # =====================================================
    # CREAR INTERFAZ
    # =====================================================
    def construir_ui(self):

        # Contenedor
        container = tk.Frame(self.frame, bg="white")
        container.pack(fill="both", expand=True)

        container.grid_columnconfigure(0, weight=0)  # Imagen izquierda
        container.grid_columnconfigure(1, weight=1)  # Formulario derecha

        # ============================
        # IMAGEN IZQUIERDA
        # ============================
        left = tk.Frame(container, bg="white")
        left.grid(row=0, column=0, sticky="ns")

        img = Image.open("assets/login_bg.jpg")
        img = img.resize((500, 600))
        self.img = ImageTk.PhotoImage(img)

        tk.Label(left, image=self.img).pack(fill="both", expand=True)

        # ============================
        # FORMULARIO DERECHA
        # ============================
        right = tk.Frame(container, bg="white")
        right.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)

        right.grid_columnconfigure(0, weight=1)

        # Contenedor para centrar formulario
        form = tk.Frame(right, bg="white")
        form.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        tk.Label(form, text="Inicio de sesión",
                 font=("Arial", 28, "bold"), bg="white").pack(pady=20)

        # Usuario
        tk.Label(form, text="Usuario", font=("Arial", 14), bg="white").pack(anchor="w")
        self.ent_usuario = ttk.Entry(form, width=30)
        self.ent_usuario.pack(pady=(0, 10))

        # Contraseña
        tk.Label(form, text="Contraseña", font=("Arial", 14), bg="white").pack(anchor="w")
        self.ent_contra = ttk.Entry(form, width=30, show="*")
        self.ent_contra.pack(pady=(0, 10))

        ttk.Button(form, text="Ingresar", command=self.login_manual).pack(pady=20)

        # Texto asistente
        self.label_transcripcion = tk.Label(form, text="", fg="gray", bg="white")
        self.label_transcripcion.pack()

        # Crear asistente
        self.asistente = VozAsistente(
            ui_callback_transcripcion=self.mostrar,
            ui_callback_comando=self.procesar
        )

    # =====================================================
    # ASISTENTE DE VOZ
    # =====================================================
    def iniciar_asistente(self):
        mensaje = (
            "Bienvenido al login. "
            "Dime tu usuario y contraseña juntos. Por ejemplo: Karen uno dos tres."
        )

        self.label_transcripcion.config(text=mensaje)
        self.asistente.hablar(mensaje)
        self.asistente.activar()

    def mostrar(self, texto):
        self.label_transcripcion.config(text=f"Escuchando: {texto}")

    # =====================================================
    # VALIDACIÓN REAL
    # =====================================================
    def validar_usuario(self, usuario, contrasena):
        usuario = usuario.lower()

        if usuario not in usuarios:
            self.asistente.hablar("Usuario no encontrado.")
            return None

        if usuarios[usuario]["password"] != contrasena:
            self.asistente.hablar("Contraseña incorrecta.")
            return None

        return usuarios[usuario]

    # =====================================================
    # NORMALIZAR CONTRASEÑA HABLADA
    # =====================================================
    def normalizar_contrasena(self, texto):
        reemplazos = {
            "uno": "1", "dos": "2", "tres": "3",
            "cuatro": "4", "cinco": "5", "seis": "6",
            "siete": "7", "ocho": "8", "nueve": "9",
            "cero": "0"
        }

        palabras = texto.lower().split()
        resultado = ""

        for p in palabras:
            resultado += reemplazos.get(p, p)

        return resultado

    # =====================================================
    # PROCESAR COMANDO DE VOZ
    # =====================================================
    def procesar(self, texto):
        partes = texto.split()

        if len(partes) < 2:
            self.asistente.hablar("Por favor di usuario y contraseña juntos.")
            return

        usuario = partes[0].lower()
        contrasena = self.normalizar_contrasena(" ".join(partes[1:]))

        # Rellenar UI
        self.ent_usuario.delete(0, tk.END)
        self.ent_usuario.insert(0, usuario)

        self.ent_contra.delete(0, tk.END)
        self.ent_contra.insert(0, contrasena)

        # Validación
        datos = self.validar_usuario(usuario, contrasena)
        if datos is None:
            return

        self.asistente.hablar(f"Bienvenido {datos['nombre']}. Ingresando ahora.")

        self.root.after(1500, lambda: self.callback_login(datos, datos["rol"]))

    # =====================================================
    # LOGIN MANUAL
    # =====================================================
    def login_manual(self):
        usuario = self.ent_usuario.get().lower()
        contrasena = self.ent_contra.get()

        datos = self.validar_usuario(usuario, contrasena)
        if datos is None:
            return

        self.callback_login(datos, datos["rol"])
