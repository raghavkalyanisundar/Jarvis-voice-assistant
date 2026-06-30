import pyttsx3
import sounddevice as sd
import numpy as np
import speech_recognition as sr

#this function records the given data from speech or microphone input function
def listen():
    recognizer = sr.Recognizer()

    fs = 44100
    silence_threshold = 50
    silence_limit = 3.0
    max_time = 30
    chunk_duration=0.4
    initial_grace_period = 6.0

    print("\nListening...")
    
    audio_buffer = []
    silence_time = 0
    total_time = 0
    chunk_size = int(0.4 * fs)

    stream = sd.InputStream(
        samplerate=fs,
        channels=1,
        dtype='int16'
    )

    with stream:
        while True:
            chunk, _ = stream.read(chunk_size)
            audio_buffer.append(chunk)
            total_time += 0.4

            volume = np.abs(chunk).mean()

            if total_time < initial_grace_period:
                silence_time =0
            else:
                if volume < silence_threshold:
                    silence_time+=0.4
                else:
                    silence_time=0

            if silence_time >= silence_limit:
                print("Silence detected, stopping.")
                break

            if total_time >= max_time:
                print("Max duration reached, stopping.")
                break

    audio_np = np.concatenate(audio_buffer, axis=0)
    audio_bytes = audio_np.tobytes()
    audio_data = sr.AudioData(audio_bytes, fs, 2)

    print("Processing...")

    try:
        text = recognizer.recognize_google(audio_data)
        print("You said:", text)
        return text
    

    # error detectors that will return a text to figure out the type of error if occured.

    except sr.UnknownValueError:
        print("Speech could not be understood.")
        return ""

    except sr.RequestError as e:
        print("Speech service error:", e)
        return ""

    except Exception as e:
        print("Unexpected error:", e)
        return ""






# the speak function makes JARVIS talk by loading text into Ai engine and then returns text

def speak(text):
    engine = pyttsx3.init()   # NEW engine every time
    engine.say(text)
    engine.runAndWait()
    engine.stop() 