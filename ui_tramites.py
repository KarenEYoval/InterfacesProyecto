import tkinter as tk
from tkinter import ttk
from Voz_Asistente import VozAsistente


class TramitesUI:
    def __init__(self, root, callback_navegar):
        self.root = root
        self.callback_navegar = callback_navegar

        root.title("Gestión de trámites")
        root.geometry("1000x650")
        root.config(bg="#f4f4f4")

        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        # ✅ Reusar asistente del login
        self.asistente = root.asistente
        self.asistente.callback_transcripcion = self.transcribir
        self.asistente.callback_comando = self.procesar_comando

        self.construir_ui()

        # 🔥 Activar mensaje de bienvenida
        root.after(800, self.iniciar_asistente)

    # ---------------------- UI ----------------------

    def construir_ui(self):
        barra = tk.Frame(self.frame, bg="#0057A3", height=80)
        barra.pack(fill="x")
        tk.Label(
            barra, text="Gestión de trámites",
            font=("Arial", 28, "bold"),
            bg="#0057A3", fg="white"
        ).pack(pady=15)

        # --- Menú lateral ---
        menu = tk.Frame(self.frame, bg="white")
        menu.pack(side="left", fill="y")

        def boton(texto, destino):
            return tk.Button(menu, text=texto, font=("Arial", 16),
                             bg="#0DA24E", fg="white",
                             activebackground="#0C8C42",
                             width=15, height=4,
                             command=lambda: self.navegar(destino))

        boton("Inicio", "inicio").pack(fill="x")
        boton("Estado de\ntrámites", "estado").pack(fill="x")
        boton("Historial", "historial").pack(fill="x")

        # --- Contenido principal ---
        contenido = tk.Frame(self.frame, bg="white")
        contenido.pack(side="right", fill="both", expand=True, padx=40)

        tk.Label(
            contenido, text="Solicitar trámite",
            font=("Arial", 24, "bold"),
            bg="white"
        ).pack(anchor="w", pady=30)

        # --- Combo de trámites ---
        self.combo = ttk.Combobox(
            contenido,
            state="readonly",
            values=[
                "Alta de experiencia educativa",
                "Baja de experiencia educativa",
                "Examen extraordinario",
                "Título de suficiencia"
            ],
            font=("Arial", 12)
        )
        self.combo.set("Selecciona el tipo de trámite")
        self.combo.pack(pady=10)

        # --- Requisitos ---
        tk.Label(
            contenido, text="Requisitos",
            font=("Arial", 20, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(30, 5))

        self.lista_req = tk.Frame(contenido, bg="white")
        self.lista_req.pack(anchor="w")

        self.actualizar_requisitos(None)

        # --- Botón siguiente ---
        tk.Button(
            contenido, text="Siguiente",
            font=("Arial", 14, "bold"),
            bg="#0057A3", fg="white",
            activebackground="#004A88",
            padx=20, pady=6
        ).pack(pady=40)

        # Transcripción
        self.transcripcion_lbl = tk.Label(
            contenido, text="",
            fg="gray", bg="white",
            font=("Arial", 12)
        )
        self.transcripcion_lbl.pack()

        tk.Button(
            contenido, text="🎤 Iniciar asistente",
            font=("Arial", 12),
            bg="#0DA24E", fg="white",
            command=self.asistente.activar
        ).pack(pady=5)

    # -------------------- ASISTENTE --------------------

    def iniciar_asistente(self):

        # 1️⃣ Detener escucha previa
        try:
            self.asistente.detener()
        except:
            pass

        # 2️⃣ Mensaje de bienvenida
        mensaje = (
            "Bienvenido a la ventana de trámites. "
            "¿Qué trámite deseas hacer? Puedes elegir: "
            "examen extraordinario, examen título de suficiencia, "
            "alta de experiencia educativa o baja de experiencia educativa."
        )

        # 3️⃣ Hablar primero (sin micrófono activo)
        self.asistente.hablar(mensaje)

        # 4️⃣ Activar escucha después
        self.root.after(2000, self.asistente.activar)

    def transcribir(self, texto):
        self.transcripcion_lbl.config(text=f"Escuchando: {texto}")

    def procesar_comando(self, texto):

        t = texto.lower()

        # ---- Alta ----
        if "alta" in t:
            tramite = "Alta de experiencia educativa"
            self.combo.set(tramite)
            self.asistente.hablar("Trámite seleccionado: alta de experiencia educativa.")
            self.actualizar_requisitos(tramite)
            return

        # ---- Baja ----
        if "baja" in t:
            tramite = "Baja de experiencia educativa"
            self.combo.set(tramite)
            self.asistente.hablar("Trámite seleccionado: baja de experiencia educativa.")
            self.actualizar_requisitos(tramite)
            return

        # ---- Extraordinario ----
        if "extra" in t or "extraordinario" in t:
            tramite = "Examen extraordinario"
            self.combo.set(tramite)
            self.asistente.hablar("Trámite seleccionado: examen extraordinario.")
            self.actualizar_requisitos(tramite)
            return

        # ---- Suficiencia ----
        if "suficiencia" in t or "título" in t or "titulo" in t:
            tramite = "Título de suficiencia"
            self.combo.set(tramite)
            self.asistente.hablar("Trámite seleccionado: título de suficiencia.")
            self.actualizar_requisitos(tramite)
            return

        # ---- Navegación ----
        if "inicio" in t:
            self.asistente.hablar("Regresando al inicio.")
            self.navegar("inicio")

        if "estado" in t:
            self.asistente.hablar("Mostrando estado de trámites.")
            self.navegar("estado")

        if "historial" in t:
            self.asistente.hablar("Abriendo historial.")
            self.navegar("historial")

    # ------------------ REQUISITOS ------------------

    def actualizar_requisitos(self, tramite):
        for w in self.lista_req.winfo_children():
            w.destroy()

        reqs = {
            "Alta de experiencia educativa": [
                "Formulario de alta firmado",
                "Motivo de la alta",
                "Constancia académica"
            ],
            "Baja de experiencia educativa": [
                "Solicitud de baja",
                "Motivo de la baja",
                "Sin adeudos en la materia"
            ],
            "Examen extraordinario": [
                "Pago del examen extraordinario",
                "Identificación oficial",
                "Registro de calificaciones"
            ],
            "Título de suficiencia": [
                "Solicitud de título de suficiencia",
                "Pago correspondiente",
                "Historial académico vigente"
            ],
        }

        lista = reqs.get(tramite, ["Selecciona un trámite para ver requisitos."])

        for r in lista:
            fila = tk.Frame(self.lista_req, bg="white")
            fila.pack(anchor="w")
            tk.Label(fila, text="●", fg="gray", bg="white",
                     font=("Arial", 14)).pack(side="left")
            tk.Label(fila, text=r, bg="white",
                     font=("Arial", 14)).pack(side="left")

    # ------------------ NAVEGACIÓN ------------------

    def navegar(self, destino):
        self.callback_navegar(destino)
