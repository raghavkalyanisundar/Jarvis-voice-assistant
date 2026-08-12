from PySide6.QtCore import QThread, Signal
import time
from voice import listen, speak
from brain import ask_jarvis
import commands
import sounddevice as sd
from openwakeword.model import Model
import logging






logging.basicConfig(
    filename="jarvis_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class AssistantThread(QThread):
    # ---- these are the "announcements" this thread can send to the UI ----
    status_changed = Signal(str)
    heard_text = Signal(str)
    classified = Signal(str)
    replied_text = Signal(str)
    log_message = Signal(str)
    app_should_quit = Signal()
    show_window = Signal()
    hide_window = Signal()

    def run(self):
        oww_model = Model(wakeword_models=["hey_jarvis_v0.1"])


        while True:
            try:
                self.status_changed.emit("JARVIS")
                self.log_message.emit("Waiting for wake word...")
                self.wait_for_wake_word(oww_model)

                self.log_message.emit("Wake word detected!")
                self.status_changed.emit("LISTENING")
                self.show_window.emit()
                speak("Yes")
                time.sleep(0.2)

                empty_count = 0

                while True:
                    user_input = listen()

                    if not user_input:
                        empty_count += 1
                        if empty_count >= 3:
                            self.log_message.emit("No response, going back to sleep.")
                            break
                        continue

                    empty_count = 0
                    self.heard_text.emit(user_input)

                    if user_input.lower() == "exit":
                        self.log_message.emit("Goodbye")
                        speak("Goodbye.")
                        logging.info("Exit command received. Shutting down.")
                        self.app_should_quit.emit()
                        return

                    if user_input.lower() in ("go to sleep", "goodbye jarvis", "stop listening"):
                        self.log_message.emit("Going back to sleep.")
                        speak("Okay.")
                        self.hide_window.emit()
                        break

                    self.status_changed.emit("THINKING")
                    mode = commands.route(user_input)
                    self.classified.emit(mode)

                    if mode == "command":
                        self.log_message.emit("command")
                        self.replied_text.emit("Command executed.")
                        self.status_changed.emit("SPEAKING")
                        speak("command")
                    else:
                        reply = ask_jarvis(user_input)
                        self.replied_text.emit(reply)
                        self.status_changed.emit("SPEAKING")
                        speak(reply)
                        time.sleep(0.1)

                    self.status_changed.emit("LISTENING")
                

            except Exception as e:
                logging.exception("Error in assistant loop:")
                self.log_message.emit(f"ERROR: {e}")
                self.status_changed.emit("ERROR")
                time.sleep(1)



    def wait_for_wake_word(self, oww_model):
        """Blocks here, passively listening, until 'hey jarvis' is detected."""
        detected = False
        chunk_count = 0
        warmup_chunks = 15  # ignore roughly the first ~1.2 seconds of audio

        def audio_callback(indata, frames, time_info, status):
            nonlocal detected, chunk_count
            chunk_count += 1

            audio_chunk = indata[:, 0]
            prediction = oww_model.predict(audio_chunk)

            if chunk_count <= warmup_chunks:
                return
            
            for wake_word, score in prediction.items():
                if score > 0.5:
                    detected = True

        with sd.InputStream(
            samplerate=16000,
            channels=1,
            dtype='int16',
            blocksize=1280,
            callback=audio_callback
        ):
            while not detected:
                time.sleep(0.05)