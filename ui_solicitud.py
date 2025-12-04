import tkinter as tk
from utilidades_pdf import generar_pdf
from ui_tramites import TramitesUI


class SolicitudUI:
    def __init__(self, root, datos_usuario):
        self.root = root
        self.datos = datos_usuario

        # Reusar asistente
        self.asistente = getattr(root, "asistente", None)

        root.title("Llenado de solicitud")
        root.config(bg="white")

        self.materia_seleccionada = None

        # ===== FRAME PRINCIPAL =====
        frame = tk.Frame(root, bg="white")
        frame.pack(fill="both", expand=True)

        # ===== BARRA SUPERIOR =====
        barra = tk.Frame(frame, bg="#0057A3", height=70)
        barra.pack(fill="x")
        tk.Label(
            barra,
            text="Llenado de solicitud",
            font=("Arial", 24, "bold"),
            bg="#0057A3",
            fg="white"
        ).pack(pady=15)

        # ===== CONTENIDO =====
        contenido = tk.Frame(frame, bg="white")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)

        contenido.grid_columnconfigure(0, weight=1)
        contenido.grid_columnconfigure(1, weight=1)

        # ---------- DATOS DEL ALUMNO ----------
        datos_alumno = tk.LabelFrame(
            contenido,
            text="Datos del alumno",
            bg="white",
            font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        datos_alumno.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(
            datos_alumno,
            text=f"Nombre del alumno(a):\n  {self.datos['nombre']}",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor="w", pady=5)

        tk.Label(
            datos_alumno,
            text=f"Matrícula:\n  {self.datos['matricula']}",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor="w", pady=5)

        # ---------- DATOS ACADEMIA ----------
        datos_academia = tk.LabelFrame(
            contenido,
            text="Datos de academia",
            bg="white",
            font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        datos_academia.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(
            datos_academia,
            text=f"Carrera:\n  {self.datos['carrera']}",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor="w", pady=5)

        # ---------- MATERIAS DEL ALUMNO ----------
        frame_materias = tk.LabelFrame(
            contenido,
            text="Materias registradas",
            bg="white",
            font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        frame_materias.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        tabla = tk.Frame(frame_materias, bg="white")
        tabla.pack()

        tk.Label(
            tabla, text="NRC", width=20,
            borderwidth=1, relief="solid",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0)

        tk.Label(
            tabla, text="Nombre", width=40,
            borderwidth=1, relief="solid",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1)

        fila = 1
        for materia in self.datos.get("materias", []):
            tk.Label(
                tabla, text=materia["nrc"], width=20,
                borderwidth=1, relief="solid", font=("Arial", 11)
            ).grid(row=fila, column=0)
            tk.Label(
                tabla, text=materia["nombre"], width=40,
                borderwidth=1, relief="solid", font=("Arial", 11)
            ).grid(row=fila, column=1)
            fila += 1

        # ---------- SELECCIÓN DE MATERIA ----------
        frame_alta = tk.LabelFrame(
            contenido,
            text="Selecciona la materia que quieres dar de alta",
            bg="white",
            font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        frame_alta.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.materia_var = tk.StringVar(value="")

        opciones = [
            "Base de datos",
            "Integración de soluciones",
            "Interfaces",
            "Seguridad"
        ]

        for op in opciones:
            tk.Radiobutton(
                frame_alta, text=op, value=op,
                variable=self.materia_var, bg="white",
                font=("Arial", 12), anchor="w",
                command=self.on_seleccionar_materia
            ).pack(anchor="w", pady=3)

        tk.Label(
            frame_alta,
            text="Di la materia o selecciónala y luego di 'siguiente'.",
            font=("Arial", 11), bg="white", fg="gray"
        ).pack(anchor="w", pady=5)

        # BOTÓN SIGUIENTE
        tk.Button(
            frame,
            text="Siguiente",
            bg="#0057A3", fg="white",
            font=("Arial", 14, "bold"),
            padx=20, pady=6,
            command=self.confirmar_materia
        ).pack(pady=20)

        # Transcripción
        self.transcripcion_lbl = tk.Label(
            frame, text="", font=("Arial", 11), bg="white", fg="gray"
        )
        self.transcripcion_lbl.pack()

        # Activar asistente
        if self.asistente:
            self.asistente.limpiar_callbacks()
            self.asistente.callback_transcripcion = self.transcribir
            self.asistente.callback_comando = self.procesar_comando
            root.after(800, self.iniciar_asistente)

    # ======================================================
    # ASISTENTE DE VOZ
    # ======================================================
    def iniciar_asistente(self):
        if not self.asistente:
            return

        mensaje = (
            "¿Qué materia quieres dar de alta? "
            "Puedes elegir: Base de datos, Integración de soluciones, "
            "Interfaces o Seguridad. Después di 'siguiente'."
        )
        self.asistente.hablar(mensaje)
        self.root.after(600, self.asistente.activar)

    def transcribir(self, texto):
        self.transcripcion_lbl.config(text=f"Escuchando: {texto}")

    def procesar_comando(self, texto):
        t = texto.lower()

        # Detectar materia
        if "base" in t:
            self.materia_var.set("Base de datos")
            self.on_seleccionar_materia()
            return

        if "integracion" in t or "integración" in t:
            self.materia_var.set("Integración de soluciones")
            self.on_seleccionar_materia()
            return

        if "interface" in t or "interfaces" in t:
            self.materia_var.set("Interfaces")
            self.on_seleccionar_materia()
            return

        if "seguridad" in t:
            self.materia_var.set("Seguridad")
            self.on_seleccionar_materia()
            return

        # Detectar "siguiente"
        if any(p in t for p in [
            "siguiente", "sigiente", "siguente",
            "continuar", "adelante", "ok", "prosigue"
        ]):
            self.confirmar_materia()
            return

    # ======================================================
    # SELECCIÓN MATERIA
    # ======================================================
    def on_seleccionar_materia(self):
        self.materia_seleccionada = self.materia_var.get()
        if self.asistente and self.materia_seleccionada:
            self.asistente.hablar(
                f"Has seleccionado la materia {self.materia_seleccionada}."
            )
            self.root.after(500, self.asistente.activar)

    # ======================================================
    # CONFIRMAR Y GENERAR PDF
    # ======================================================
    def confirmar_materia(self):
        materia = self.materia_var.get()

        if not materia:
            if self.asistente:
                self.asistente.hablar(
                    "Por favor indica qué materia quieres dar de alta."
                )
                self.root.after(500, self.asistente.activar)
            return

        # Apagar asistente
        if self.asistente and self.asistente.escuchando:
            self.asistente.detener()

        # Generar PDF
        nombre_pdf = f"alta_{self.datos['matricula']}.pdf"
        generar_pdf(
            nombre_archivo=nombre_pdf,
            titulo="SOLICITUD DE ALTA DE EXPERIENCIA EDUCATIVA",
            datos_alumno=self.datos,
            tramite="Alta de experiencia educativa",
            materia=materia
        )

        if self.asistente:
            self.asistente.hablar(
                f"Materia {materia} dada de alta. "
                "Tu comprobante PDF ha sido generado."
            )

        # Regresar al menú principal
        self.root.after(2000, self.volver_menu)

    # ======================================================
    # VOLVER A MENÚ
    # ======================================================
    def volver_menu(self):
        if self.asistente:
            if self.asistente.escuchando:
                self.asistente.detener()
            self.asistente.limpiar_callbacks()

        for widget in self.root.winfo_children():
            widget.destroy()

        TramitesUI(self.root, lambda *args: None, self.datos)
