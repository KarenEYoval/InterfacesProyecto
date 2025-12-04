import speech_recognition as sr
import pyttsx3
import threading

class VozAsistente:
    def __init__(self, ui_callback_transcripcion, ui_callback_comando):
        self.callback_transcripcion = ui_callback_transcripcion
        self.callback_comando = ui_callback_comando
        self.escuchando = False

        # Motor de voz
        self.engine = pyttsx3.init()

        # Arreglo para que funcione la voz en Windows
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170)

    # ----------------- HABLAR -----------------

    def hablar(self, texto):
        try:
            print("Asistente dice:", texto)
            self.engine.say(texto)
            self.engine.runAndWait()
        except Exception as e:
            print("ERROR hablando:", e)

    # ----------------- ACTIVAR ASISTENTE -----------------

    def activar(self):
        """Activa micrófono + habla el mensaje inicial"""
        try:
            self.hablar("Bienvenido al login. Dime tu usuario.")
        except:
            print("No se pudo reproducir voz")

        self.escuchando = True
        hilo = threading.Thread(target=self.escuchar, daemon=True)
        hilo.start()

    # ----------------- ESCUCHAR -----------------

    def escuchar(self):
        r = sr.Recognizer()

        while self.escuchando:
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source)

                texto = r.recognize_google(audio, language="es-MX")

                # Mandarlo a la UI
                self.callback_transcripcion(texto)
                self.callback_comando(texto)

            except Exception:
                pass
