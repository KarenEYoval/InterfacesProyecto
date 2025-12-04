import tkinter as tk


class SolicitudUI:
    def __init__(self, root, datos_usuario):
        self.root = root
        self.datos = datos_usuario

        root.title("Llenado de solicitud")
        root.geometry("1000x650")
        root.config(bg="white")

        frame = tk.Frame(root, bg="white")
        frame.pack(fill="both", expand=True)

        # Título
        tk.Label(frame, text="Llenado de solicitud",
                 font=("Arial", 28, "bold"),
                 bg="#0057A3", fg="white").pack(fill="x")

        # DATOS DEL ALUMNO
        tk.Label(frame, text="Datos del alumno",
                 font=("Arial", 20, "bold"),
                 bg="white").pack(anchor="w", padx=20, pady=(20, 5))

        tk.Label(frame, text=f"Nombre del alumno(a):\n  {self.datos['nombre']}",
                 font=("Arial", 14), bg="white").pack(anchor="w", padx=20)

        tk.Label(frame, text=f"Matrícula:\n  {self.datos['matricula']}",
                 font=("Arial", 14), bg="white").pack(anchor="w", padx=20, pady=10)

        # DATOS DE ACADEMIA
        tk.Label(frame, text="Datos de academia",
                 font=("Arial", 20, "bold"),
                 bg="white").pack(anchor="w", padx=20)

        tk.Label(frame, text=f"Carrera:\n  {self.datos['carrera']}",
                 font=("Arial", 14), bg="white").pack(anchor="w", padx=20, pady=5)

        # EXPERIENCIA EDUCATIVA
        tk.Label(frame, text="Datos de la Experiencia educativa",
                 font=("Arial", 20, "bold"),
                 bg="white").pack(anchor="w", padx=20, pady=20)

        tabla = tk.Frame(frame, bg="white")
        tabla.pack()

        tk.Label(tabla, text="NRC", width=20, borderwidth=1, relief="solid",
                 font=("Arial", 12, "bold")).grid(row=0, column=0)
        tk.Label(tabla, text="Nombre", width=40, borderwidth=1, relief="solid",
                 font=("Arial", 12, "bold")).grid(row=0, column=1)

        fila = 1
        for materia in self.datos["materias"]:
            tk.Label(tabla, text=materia["nrc"], width=20, borderwidth=1,
                     relief="solid", font=("Arial", 12)).grid(row=fila, column=0)
            tk.Label(tabla, text=materia["nombre"], width=40, borderwidth=1,
                     relief="solid", font=("Arial", 12)).grid(row=fila, column=1)
            fila += 1

        # BOTÓN SIGUIENTE
        tk.Button(frame, text="Siguiente",
                  bg="#0057A3", fg="white",
                  font=("Arial", 14, "bold"),
                  padx=20, pady=6).pack(pady=20)
