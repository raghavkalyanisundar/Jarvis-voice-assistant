
## Jarvis- Local Ai voice assistant

A voice-controlled AI assistant that runs fully on my own computer, inspired by JARVIS from Iron Man.


<img width="1500" height="842" alt="image" src="https://github.com/user-attachments/assets/88edf3fa-6364-4d2d-8aed-87e09e8cfd1e" />


## Features
- Wake word activation ("Hey JARVIS")
- Runs a local AI model through Ollama (no cloud needed)
- Speech recognition and text-to-speech responses
- Custom user interface


## How It Works
JARVIS listens for a wake word, then uses speech recognition to turn your voice into text. That text is sent to a local AI model running through Ollama, so everything runs on your own computer without the cloud. A Python bridge connects the AI to a custom user interface, where responses are displayed and spoken back using text-to-speech. Each part of the system is split into its own module, which makes it easier to add new features, like the robotic arm integration I'm currently working on.

