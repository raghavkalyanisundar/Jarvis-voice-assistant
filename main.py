from brain import ask_jarvis
from voice import speak

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":

        print("Jarvis: Goodbye.")
        speak("Goodbye.")
        break

    reply = ask_jarvis(user_input)

    print("Jarvis:", reply)

    speak(reply)