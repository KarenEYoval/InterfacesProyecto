import tkinter as tk
from utilidades_pdf import generar_pdf
from ui_tramites import TramitesUI


class TituloUI:
    def __init__(self, root, datos_usuario):
        self.root = root
        self.datos = datos_usuario

        self.asistente = getattr(root, "asistente", None)
        self.materia_seleccionada = None

        root.title("Solicitud de Título de Suficiencia")
        root.config(bg="white")

        frame = tk.Frame(root, bg="white")
        frame.pack(fill="both", expand=True)

        # ===== TÍTULO =====
        barra = tk.Frame(frame, bg="#0057A3", height=70)
        barra.pack(fill="x")
        tk.Label(
            barra,
            text="Solicitud de Título de Suficiencia",
            font=("Arial", 24, "bold"),
            bg="#0057A3",
            fg="white"
        ).pack(pady=15)

        contenido = tk.Frame(frame, bg="white")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)

        contenido.grid_columnconfigure(0, weight=1)
        contenido.grid_columnconfigure(1, weight=1)

        # ---------- DATOS DEL ALUMNO ----------
        datos_alumno = tk.LabelFrame(
            contenido, text="Datos del alumno",
            bg="white", font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        datos_alumno.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(datos_alumno,
                 text=f"Nombre:\n  {self.datos['nombre']}",
                 bg="white", font=("Arial", 12)).pack(anchor="w")

        tk.Label(datos_alumno,
                 text=f"Matrícula:\n  {self.datos['matricula']}",
                 bg="white", font=("Arial", 12)).pack(anchor="w")

        tk.Label(datos_alumno,
                 text=f"Carrera:\n  {self.datos['carrera']}",
                 bg="white", font=("Arial", 12)).pack(anchor="w")

        # ---------- MATERIAS ----------
        frame_materias = tk.LabelFrame(
            contenido,
            text="Selecciona la materia del título de suficiencia",
            bg="white", font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        frame_materias.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.materia_var = tk.StringVar(value="")

        for m in self.datos["materias"]:
            tk.Radiobutton(
                frame_materias,
                text=m["nombre"],
                value=m["nombre"],
                variable=self.materia_var,
                bg="white",
                font=("Arial", 12),
                anchor="w",
                command=self.on_materia
            ).pack(anchor="w")

        self.info = tk.Label(
            frame_materias,
            text="Puedes seleccionar con clic o por voz.\nDi: 'título en ___'.",
            bg="white", fg="gray", font=("Arial", 10)
        )
        self.info.pack(anchor="w")

        # ---------- BOTÓN ----------
        tk.Button(
            frame, text="Siguiente",
            bg="#0057A3", fg="white",
            font=("Arial", 14, "bold"),
            padx=20, pady=6,
            command=self.confirmar_titulo
        ).pack(pady=20)

        # ---------- TRANSCRIPCIÓN ----------
        self.transcripcion_lbl = tk.Label(
            frame, text="", bg="white", fg="gray", font=("Arial", 11)
        )
        self.transcripcion_lbl.pack()

        # ---------- ASISTENTE ----------
        if self.asistente:
            self.asistente.callback_transcripcion = self.transcribir
            self.asistente.callback_comando = self.procesar_comando
            root.after(800, self.iniciar_asistente)

    # ====================================================
    # ASISTENTE
    # ====================================================
    def iniciar_asistente(self):
        materias = ", ".join([m["nombre"] for m in self.datos["materias"]])
        mensaje = (
            "Solicitud de título de suficiencia. "
            "Puedes elegir alguna de tus materias actuales: "
            f"{materias}. Para seleccionar, di el nombre. "
            "Después di 'siguiente' para continuar."
        )

        self.asistente.hablar(mensaje)
        self.asistente.activar()

    def transcribir(self, texto):
        self.transcripcion_lbl.config(text=f"Escuchando: {texto}")

    def procesar_comando(self, texto):
        t = texto.lower()

        for m in self.datos["materias"]:
            if m["nombre"].lower().split()[0] in t:
                self.materia_var.set(m["nombre"])
                self.on_materia()
                return

        if "siguiente" in t:
            self.confirmar_titulo()

    # ====================================================
    # Selección materia
    # ====================================================
    def on_materia(self):
        self.materia_seleccionada = self.materia_var.get()
        if self.asistente:
            self.asistente.hablar(f"Has seleccionado {self.materia_seleccionada}.")

    # ====================================================
    # GENERAR PDF Y REGRESAR AL MENÚ
    # ====================================================
    def confirmar_titulo(self):
        if not self.materia_var.get():
            self.asistente.hablar("Selecciona una materia primero.")
            return

        try:
            self.asistente.detener()
        except:
            pass

        materia = self.materia_var.get()
        tramite = "Título de Suficiencia"

        archivo = generar_pdf(
            nombre_archivo=f"titulo_{self.datos['matricula']}.pdf",
            titulo="SOLICITUD DE TÍTULO DE SUFICIENCIA",
            datos_alumno=self.datos,
            tramite=tramite,
            materia=materia
        )

        self.asistente.hablar(
            f"Título de suficiencia para {materia} registrado. "
            "Tu comprobante en PDF ha sido generado."
        )

        self.root.after(2000, self.volver_menu)

    # ====================================================
    def volver_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        TramitesUI(self.root, lambda *args: None, self.datos)
