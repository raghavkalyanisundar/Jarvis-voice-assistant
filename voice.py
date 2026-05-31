import pyttsx3

import sounddevice as sd
import numpy as np
import speech_recognition as sr


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
        print("You said:")


engine = pyttsx3.init()

def speak(text):

    engine.say(text)
    engine.runAndWait()