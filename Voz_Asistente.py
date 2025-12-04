import speech_recognition as sr
import pyttsx3
import threading

class VozAsistente:
    def __init__(self, ui_callback_transcripcion, ui_callback_comando):
        self.callback_transcripcion = ui_callback_transcripcion
        self.callback_comando = ui_callback_comando
        self.escuchando = False

        # Motor de voz (si lo necesitas luego)
        self.engine = pyttsx3.init()

    def hablar(self, texto):
        self.engine.say(texto)
        self.engine.runAndWait()

    def activar(self):
        """Activa el reconocimiento sin decir nada."""
        self.escuchando = True
        threading.Thread(target=self.escuchar, daemon=True).start()

    def escuchar(self):
        r = sr.Recognizer()

        while self.escuchando:
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source)

                texto = r.recognize_google(audio, language="es-MX")

                # Mostrar transcripción en pantalla
                self.callback_transcripcion(texto)

                # Enviar comando al LoginUI
                self.callback_comando(texto)

            except Exception:
                pass
