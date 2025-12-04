import tkinter as tk
from tkinter import ttk
from utilidades import centrar_ventana



class TramitesUI:
    def __init__(self, root, callback_navegar, datos_usuario):
        self.datos_usuario = datos_usuario
        self.root = root
        centrar_ventana(root, 500, 500)
        self.callback_navegar = callback_navegar

        root.title("Gestión de trámites")
        root.geometry("1000x650")
        root.config(bg="#f4f4f4")
        

        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        # Reusar asistente del login
        self.asistente = root.asistente
        self.asistente.callback_transcripcion = self.transcribir
        self.asistente.callback_comando = self.procesar_comando

        self.tramite_seleccionado = None

        self.construir_ui()
        root.after(800, self.iniciar_asistente)
        


    #=========================================================
    # UI
    #=========================================================
    def construir_ui(self):
        barra = tk.Frame(self.frame, bg="#0057A3", height=80)
        barra.pack(fill="x")

        tk.Label(
            barra, text="Gestión de trámites",
            font=("Arial", 28, "bold"), bg="#0057A3", fg="white"
        ).pack(pady=15)

        contenido = tk.Frame(self.frame, bg="white")
        contenido.pack(fill="both", expand=True)

        tk.Label(
            contenido, text="Selecciona un trámite",
            font=("Arial", 24, "bold"), bg="white"
        ).pack(pady=20)

        # ------------------------------------------------------
        # BOTONES DE TRÁMITES (NO COMBOBOX)
        # ------------------------------------------------------
        botones_frame = tk.Frame(contenido, bg="white")
        botones_frame.pack(pady=20)

        def crear_boton(texto, valor):
            return tk.Button(
                botones_frame, text=texto,
                font=("Arial", 16), width=28, height=2,
                bg="#0DA24E", fg="white",
                activebackground="#0C8C42",
                command=lambda: self.seleccionar_tramite(valor)
            )

        crear_boton("Alta de experiencia educativa", "Alta de experiencia educativa").pack(pady=5)
        crear_boton("Baja de experiencia educativa", "Baja de experiencia educativa").pack(pady=5)
        crear_boton("Examen extraordinario", "Examen extraordinario").pack(pady=5)
        crear_boton("Título de suficiencia", "Título de suficiencia").pack(pady=5)

        # ------------------------------------------------------
        # REQUISITOS
        # ------------------------------------------------------
        tk.Label(contenido, text="Requisitos",
                 font=("Arial", 20, "bold"), bg="white").pack(pady=(20, 5))

        self.lista_req = tk.Frame(contenido, bg="white")
        self.lista_req.pack()

        self.actualizar_requisitos(None)

        # ------------------------------------------------------
        tk.Button(
            contenido, text="Siguiente",
            font=("Arial", 14, "bold"), bg="#0057A3",
            fg="white", padx=20, pady=6,
            command=self.avanzar_siguiente_pantalla
        ).pack(pady=30)

        # TRANSCRIPCIÓN
        self.transcripcion_lbl = tk.Label(
            contenido, text="", fg="gray", bg="white", font=("Arial", 12)
        )
        self.transcripcion_lbl.pack()

    #=========================================================
    # ASISTENTE
    #=========================================================
    def iniciar_asistente(self):
        self.asistente.detener()
        mensaje = (
            "Bienvenido a la ventana de trámites. "
            "Las opciones disponibles son: alta de experiencia educativa, "
            "baja de experiencia educativa, examen extraordinario "
            "y título de suficiencia."
        )
        self.asistente.hablar(mensaje)
        self.asistente.activar()

    def transcribir(self, texto):
        self.transcripcion_lbl.config(text=f"Escuchando: {texto}")

    #=========================================================
    # PROCESAR COMANDOS POR VOZ
    #=========================================================
    def procesar_comando(self, texto):
        t = texto.lower()

        if "alta" in t:
            self.seleccionar_tramite("Alta de experiencia educativa")
            return
        if "baja" in t:
            self.seleccionar_tramite("Baja de experiencia educativa")
            return
        if "extra" in t or "extraordinario" in t:
            self.seleccionar_tramite("Examen extraordinario")
            return
        if "suficiencia" in t or "titulo" in t or "título" in t:
            self.seleccionar_tramite("Título de suficiencia")
            return

        if "siguiente" in t or "continuar" in t:
            self.avanzar_siguiente_pantalla()

    #=========================================================
    # SELECCIÓN DE TRÁMITE
    #=========================================================
    def seleccionar_tramite(self, tramite):
        self.tramite_seleccionado = tramite
        self.asistente.hablar(f"Trámite seleccionado: {tramite}.")
        self.actualizar_requisitos(tramite)
        self.leer_requisitos(tramite)

    def leer_requisitos(self, tramite):
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

        mensaje = f"Los requisitos para {tramite} son: " + ", ".join(reqs[tramite])
        self.asistente.hablar(mensaje)

    #=========================================================
    # ACTUALIZAR REQUISITOS EN PANTALLA
    #=========================================================
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

    #=========================================================
    # SIGUIENTE PANTALLA
    #=========================================================
    def avanzar_siguiente_pantalla(self):
        if not self.tramite_seleccionado:
            self.asistente.hablar("Por favor selecciona un trámite antes de continuar.")
            return

        self.asistente.hablar(f"Abriendo el formulario de {self.tramite_seleccionado}.")
        self.callback_navegar("solicitud", self.datos_usuario)

