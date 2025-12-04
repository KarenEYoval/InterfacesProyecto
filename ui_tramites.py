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

        self.asistente = VozAsistente(
            ui_callback_transcripcion=self.transcribir,
            ui_callback_comando=self.procesar_comando
        )

        self.construir_ui()

    def construir_ui(self):

        # ======= BARRA SUPERIOR =======
        barra = tk.Frame(self.frame, bg="#0057A3", height=80)
        barra.pack(fill="x")
        tk.Label(barra, text="Gestion de tramites",
                 font=("Arial", 28, "bold"),
                 bg="#0057A3", fg="white").pack(pady=15)

        # ======= MENÚ LATERAL =======
        menu = tk.Frame(self.frame, bg="white")
        menu.pack(side="left", fill="y")

        def boton_menu(texto):
            return tk.Button(menu, text=texto, font=("Arial", 16),
                             bg="#0DA24E", fg="white",
                             activebackground="#0C8C42",
                             width=15, height=4)

        boton_menu("Inicio").pack(fill="x")
        boton_menu("Estado de\ntramites").pack(fill="x")
        boton_menu("Historial").pack(fill="x")

        # ======= CONTENIDO PRINCIPAL =======
        contenido = tk.Frame(self.frame, bg="white")
        contenido.pack(side="right", fill="both", expand=True, padx=40)

        tk.Label(contenido, text="Solicitar tramite",
                 font=("Arial", 24, "bold"),
                 bg="white").pack(anchor="w", pady=30)

        # Dropdown estilizado
        estilo = ttk.Style()
        estilo.configure("Custom.TMenubutton",
                         font=("Arial", 12, "bold"),
                         padding=10,
                         background="#0057A3",
                         foreground="white")

        self.combo = ttk.Combobox(contenido, state="readonly",
                                  values=[
                                      "Alta de EE",
                                      "Baja de EE",
                                      "Examen Extraordinario",
                                      "Título de suficiencia"
                                  ],
                                  font=("Arial", 12))
        self.combo.set("Selecciona el tipo de tramite")
        self.combo.pack(pady=10)

        # ======= REQUISITOS =======
        tk.Label(contenido, text="Requisitos",
                 font=("Arial", 20, "bold"),
                 bg="white").pack(anchor="w", pady=(30, 5))

        self.lista_req = tk.Frame(contenido, bg="white")
        self.lista_req.pack(anchor="w")

        reqs = ["Amar a karen", "Respetar a karen", "Darme dinero", "Jugar basket"]
        for r in reqs:
            fila = tk.Frame(self.lista_req, bg="white")
            fila.pack(anchor="w")
            tk.Label(fila, text="●", fg="gray", bg="white",
                     font=("Arial", 14)).pack(side="left")
            tk.Label(fila, text=r, bg="white",
                     font=("Arial", 14)).pack(side="left")

        # ======= BOTÓN SIGUIENTE =======
        btn = tk.Button(contenido, text="Siguiente",
                        font=("Arial", 14, "bold"),
                        bg="#0057A3", fg="white",
                        activebackground="#004A88",
                        padx=20, pady=6)
        btn.pack(pady=40)

        # ======= TRANSCRIPCIÓN DEL ASISTENTE =======
        self.transcripcion_lbl = tk.Label(contenido, text="",
                                          fg="gray", bg="white",
                                          font=("Arial", 12))
        self.transcripcion_lbl.pack()

        tk.Button(contenido, text="🎤 Iniciar asistente",
                  font=("Arial", 12),
                  bg="#0DA24E", fg="white",
                  command=self.asistente.activar).pack(pady=5)

    # ----------------------------------------------------------
    # MÉTODOS DEL ASISTENTE DE VOZ
    # ----------------------------------------------------------

    def transcribir(self, texto):
        self.transcripcion_lbl.config(text=f"Escuchando: {texto}")

    def procesar_comando(self, texto):

        t = texto.lower()

        if "tramite" in t:
            # captura selección
            if "alta" in t:
                self.combo.set("Alta de EE")
            elif "baja" in t:
                self.combo.set("Baja de EE")
            elif "extraordinario" in t:
                self.combo.set("Examen Extraordinario")
            elif "suficiencia" in t:
                self.combo.set("Título de suficiencia")

        if "siguiente" in t:
            self.asistente.hablar("Avanzando al siguiente paso.")
            print(">> Ejecutar siguiente pantalla")

        # navegación
        if "inicio" in t:
            self.asistente.hablar("Regresando al inicio.")
            self.callback_navegar("inicio")

        if "estado" in t:
            self.asistente.hablar("Mostrando estado de trámites.")
            self.callback_navegar("estado")

        if "historial" in t:
            self.asistente.hablar("Abriendo historial.")
            self.callback_navegar("historial")
