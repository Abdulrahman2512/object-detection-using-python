import pyttsx3
import time

engine = pyttsx3.init()
last_alert_time = 0

def speak_alert(text):
    global last_alert_time
    if time.time() - last_alert_time > 5:
        engine.say(text)
        engine.runAndWait()
        last_alert_time = time.time()
