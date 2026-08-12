import string
import subprocess
import webbrowser


def open_radius():
    print("Opening Radius")
    webbrowser.open("https://radius.mathnasium.com/")


def open_chrome():
    print("Opening Chrome...")
    subprocess.Popen(["start", "chrome"], shell=True)




def open_work_schedule():
    print("Opening work schedule...")
    webbrowser.open("https://appx.wheniwork.com/myschedule")


def open_spotify():
    print("opening spotify")
    subprocess.Popen(["start","spotify"], shell=True)

def open_email():
    print("opening your email")
    webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

def open_youtube():
    print("opening youtube")
    webbrowser.open("https://www.youtube.com/")


INTENTS = {
    "open_chrome": {
        "action_words": ["open", "launch", "start", "pull"],
        "target_words": ["chrome"],
        "action": open_chrome,
    },
    "open_work_schedule": {
        "action_words": ["open", "pull", "show"],
        "target_words": ["schedule"],
        "action": open_work_schedule,
    },
    "open_spotify": {
        "action_words": ["open", "launch", "start", "play"],
        "target_words": ["spotify", "music"],
        "action": open_spotify,
    },
    "open_email": {
        "action_words": ["open", "check", "pull"],
        "target_words": ["email", "mail", "gmail"],
        "action": open_email,
    },
    "open_youtube": {
        "action_words": ["open", "launch", "pull"],
        "target_words": ["youtube"],
        "action": open_youtube,
    },
    "open_radius":{
        "action_words":["open","launch","start"],
        "target_words":["radius"],
        "action":open_radius,
    },
}

def clean(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def words_close_together(words, group_a, group_b, max_distance=3):
    # find every position where a word from group_a appears
    positions_a = [i for i, w in enumerate(words) if w in group_a]
    # find every position where a word from group_b appears
    positions_b = [i for i, w in enumerate(words) if w in group_b]

    # check every pair of positions — if ANY pair is close enough, return True
    for a in positions_a:
        for b in positions_b:
            if abs(a - b) <= max_distance:
                return True
    return False


def route(text):
    text = clean(text)
    words = text.split()

    for intent_name, data in INTENTS.items():
        if words_close_together(words, data["action_words"], data["target_words"]):
            data["action"]()
            return "command"

    return "chat"