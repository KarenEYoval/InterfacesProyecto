import speech_recognition as sr
import threading
import time
import win32com.client as wincl   # <<< MOTOR DE VOZ REAL

class VozAsistente:
    def __init__(self, ui_callback_transcripcion, ui_callback_comando):
        self.callback_transcripcion = ui_callback_transcripcion
        self.callback_comando = ui_callback_comando

        # Motor de voz de Windows
        self.speaker = wincl.Dispatch("SAPI.SpVoice")

        self.escuchando = False
        self.thread_escuchar = None

    # ------------------- HABLAR -------------------
    def hablar(self, texto):
        print("Asistente dice:", texto)

        estaba_escuchando = self.escuchando
        if estaba_escuchando:
            self.detener()

        try:
            self.speaker.Speak(texto)     # <<< HABLA EN WINDOWS SIEMPRE
        except Exception as e:
            print("Error hablando:", e)

        if estaba_escuchando:
            time.sleep(0.3)
            self.activar()

    # ------------------- ACTIVAR -------------------
    def activar(self):
        if self.escuchando:
            print("⚠ Ya está escuchando.")
            return

        self.escuchando = True
        self.thread_escuchar = threading.Thread(target=self.escuchar, daemon=True)
        self.thread_escuchar.start()

    # ------------------- DETENER -------------------
    def detener(self):
        self.escuchando = False
        print("🛑 Asistente detenido")

    # ------------------- ESCUCHAR -------------------
    def escuchar(self):
        recognizer = sr.Recognizer()

        while self.escuchando:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = recognizer.listen(source)

                texto = recognizer.recognize_google(audio, language="es-MX")

                self.callback_transcripcion(texto)
                self.callback_comando(texto)

            except Exception:
                pass

            time.sleep(0.1)
