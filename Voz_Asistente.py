import speech_recognition as sr
import threading
import time
import win32com.client as wincl

class VozAsistente:
    def __init__(self, ui_callback_transcripcion, ui_callback_comando):
        self.callback_transcripcion = ui_callback_transcripcion
        self.callback_comando = ui_callback_comando

        self.speaker = wincl.Dispatch("SAPI.SpVoice")

        self.escuchando = False
        self.thread_escuchar = None

    def hablar(self, texto):
        if self.escuchando:
            self.detener()

        print("Asistente dice:", texto)

        try:
            self.speaker.Speak(texto)
        except:
            pass

    def activar(self):
        if self.escuchando:
            return
        self.escuchando = True
        self.thread_escuchar = threading.Thread(target=self.escuchar, daemon=True)
        self.thread_escuchar.start()

    def detener(self):
        self.escuchando = False
        print("🛑 Asistente detenido")

    def escuchar(self):
        recognizer = sr.Recognizer()

        while self.escuchando:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = recognizer.listen(source)

                texto = recognizer.recognize_google(audio, language="es-MX")

                self.callback_transcripcion(texto)
                self.callback_comando(texto)

            except:
                pass

            time.sleep(0.05)

    def limpiar_callbacks(self):
        self.callback_transcripcion = lambda t: None
        self.callback_comando = lambda t: None
