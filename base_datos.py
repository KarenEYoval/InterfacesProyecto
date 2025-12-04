usuarios = {

    # -------- ALUMNOS --------
    "karen": {
        "password": "123",
        "rol": "alumno",
        "nombre": "Lopez Yoval Karen Esperanza",
        "matricula": "zS22016126",
        "carrera": "Licenciatura en Tecnologías Computacionales",
        "materias": [
            {"nrc": "98342", "nombre": "Programación Avanzada"},
            {"nrc": "73122", "nombre": "Base de Datos"}
        ]
    },

    "oscar": {   # ← EN MINÚSCULAS
        "password": "abc",   # ← TAMBIÉN NORMALIZADO A MINÚSCULAS
        "rol": "alumno",
        "nombre": "Hernández Alonso Oscar",
        "matricula": "zS22022011",
        "carrera": "Ingeniería de Software",
        "materias": [
            {"nrc": "55123", "nombre": "Álgebra Lineal"},
            {"nrc": "88341", "nombre": "Ingeniería de Software I"}
        ]
    },

    # -------- SECRETARIAS --------
    "ana": {
        "password": "321",
        "rol": "secretaria",
        "nombre": "Ana Torres",
    },

    "luz": {
        "password": "999",
        "rol": "secretaria",
        "nombre": "Luz Martínez",
    }
}
