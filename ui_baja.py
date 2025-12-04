import tkinter as tk


class BajaMateriaUI:
    def __init__(self, root, datos_usuario):
        self.root = root
        self.datos = datos_usuario

        # Reusar el asistente de voz
        self.asistente = getattr(root, "asistente", None)

        self.materia_seleccionada = None

        root.title("Solicitud de Baja de Experiencia Educativa")
        root.config(bg="white")

        # ====== FRAME PRINCIPAL ======
        frame = tk.Frame(root, bg="white")
        frame.pack(fill="both", expand=True)

        # ====== BARRA SUPERIOR ======
        barra = tk.Frame(frame, bg="#A30000", height=70)
        barra.pack(fill="x")
        tk.Label(
            barra,
            text="Baja de experiencia educativa",
            font=("Arial", 24, "bold"),
            bg="#A30000",
            fg="white"
        ).pack(pady=15)

        # ====== CONTENIDO ======
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

        # ---------- MATERIAS INSCRITAS ----------
        frame_materias = tk.LabelFrame(
            contenido,
            text="Materias inscritas",
            bg="white",
            font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        frame_materias.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        tabla = tk.Frame(frame_materias, bg="white")
        tabla.pack()

        tk.Label(tabla, text="NRC", width=20, borderwidth=1, relief="solid",
                 font=("Arial", 11, "bold")).grid(row=0, column=0)
        tk.Label(tabla, text="Nombre", width=40, borderwidth=1, relief="solid",
                 font=("Arial", 11, "bold")).grid(row=0, column=1)

        fila = 1
        for materia in self.datos["materias"]:
            tk.Label(
                tabla, text=materia["nrc"],
                width=20, borderwidth=1, relief="solid",
                font=("Arial", 11)
            ).grid(row=fila, column=0)

            tk.Label(
                tabla, text=materia["nombre"],
                width=40, borderwidth=1, relief="solid",
                font=("Arial", 11)
            ).grid(row=fila, column=1)

            fila += 1

        # ---------- SELECCIÓN DE MATERIA PARA DAR DE BAJA ----------
        frame_baja = tk.LabelFrame(
            contenido,
            text="Selecciona la materia que deseas dar de baja",
            bg="white",
            font=("Arial", 14, "bold"),
            padx=10, pady=10
        )
        frame_baja.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.materia_var = tk.StringVar(value="")

        materias_disponibles = [m["nombre"] for m in self.datos["materias"]]

        for op in materias_disponibles:
            tk.Radiobutton(
                frame_baja,
                text=op,
                value=op,
                variable=self.materia_var,
                bg="white",
                font=("Arial", 12),
                anchor="w",
                command=self.on_seleccionar_materia
            ).pack(anchor="w", pady=3)

        self.label_info = tk.Label(
            frame_baja,
            text="Puedes seleccionar con clic o decir el nombre en voz alta.\nDespués di 'siguiente' para confirmar.",
            font=("Arial", 11),
            bg="white",
            fg="gray"
        )
        self.label_info.pack(anchor="w", pady=(10, 0))

        # ---------- BOTÓN SIGUIENTE ----------
        tk.Button(
            frame,
            text="Siguiente",
            bg="#A30000",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=20, pady=6,
            command=self.confirmar_baja
        ).pack(pady=20)

        # ---------- TEXTO DE TRANSCRIPCIÓN ----------
        self.transcripcion_lbl = tk.Label(
            frame, text="", font=("Arial", 11), bg="white", fg="gray"
        )
        self.transcripcion_lbl.pack(pady=(0, 10))

        # ------ ACTIVAR ASISTENTE ------
        if self.asistente:
            self.asistente.callback_transcripcion = self.transcribir
            self.asistente.callback_comando = self.procesar_comando
            self.root.after(800, self.iniciar_asistente)

    # ===================== ASISTENTE =====================
    def iniciar_asistente(self):
        if not self.asistente:
            return

        materias = ", ".join([m["nombre"] for m in self.datos["materias"]])

        mensaje = (
            "Estamos en la solicitud de baja. "
            "Puedes dar de baja cualquiera de tus materias actuales: "
            f"{materias}. "
            "Después di la palabra 'siguiente' para confirmar."
        )
        self.asistente.hablar(mensaje)
        self.asistente.activar()

    # =====================================================
    def transcribir(self, texto):
        self.transcripcion_lbl.config(text=f"Escuchando: {texto}")

    # =====================================================
    def procesar_comando(self, texto):
        t = texto.lower()

        # Intentar seleccionar por voz
        for materia in self.datos["materias"]:
            nombre = materia["nombre"].lower()
            if nombre.split()[0] in t or nombre in t:
                self.materia_var.set(materia["nombre"])
                self.on_seleccionar_materia()
                return

        # Confirmar baja
        if "siguiente" in t or "continuar" in t:
            self.confirmar_baja()

    # =====================================================
    def on_seleccionar_materia(self):
        self.materia_seleccionada = self.materia_var.get()
        if self.asistente:
            self.asistente.hablar(
                f"Has seleccionado dar de baja {self.materia_seleccionada}."
            )

    # =====================================================
    def confirmar_baja(self):
        materia = self.materia_var.get()

        if not materia:
            if self.asistente:
                self.asistente.hablar(
                    "Por favor selecciona qué materia deseas dar de baja."
                )
            return

        if self.asistente:
            self.asistente.hablar(f"Materia {materia} dada de baja correctamente.")

        print(f"Materia dada de baja: {materia}")
