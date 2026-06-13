import pyttsx3

import sounddevice as sd
import numpy as np
import speech_recognition as sr

#this function records the given data from speech or microphone input function
def listen():
    recognizer =sr.Recognizer()

    duration = 5
    print("Listening...")

    audio_data = sd.rec(int(duration*44100), samplerate=44100, channels=1, dtype='int16')
    sd.wait()
    audio_bytes=np.array(audio_data,dtype=np.int16).tobytes()
    audio=sr.AudioData(audio_bytes,44100,2)


    try:
        text = recognizer.recognize_google(audio)
        print("You said:",text)
        return text
    # when google couldn't transcribe the speech
    except sr.UnknownValueError:
        print("Sorry I didn't catch that.")
        return ""
    # occurs after common network or API errors
    except sr.RequestError:
        print("Speech recognition service error.")
        return ""






# the speak function makes JARVIS talk by loading text into Ai engine and then returns text

def speak(text):
    engine = pyttsx3.init()   # NEW engine every time
    engine.say(text)
    engine.runAndWait()
    engine.stop() 