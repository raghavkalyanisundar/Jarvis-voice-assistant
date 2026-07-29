from brain import ask_jarvis
from voice import speak, listen
import time
import commands

while True:
    time.sleep(0.2) 
    user_input = listen()

    if user_input.lower() == "exit":
        print("Goodbye")
        speak("Goodbye.")
        break

    mode = commands.route(user_input)

    if mode == "command":
        print("command")
        speak("command")


    else:
        reply = ask_jarvis(user_input)
        print(reply)
        speak(reply)
        # gives a slight delay after speaking
        time.sleep(0.1)



    