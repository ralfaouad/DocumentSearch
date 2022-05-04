# pip3 install SpeechRecognition pydub
import speech_recognition as sr

# In this file: Speech to Text

def speech2text():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio_data = r.record(source, duration=3)
        print("Recognizing...")
        try:
            text = r.recognize_google(audio_data)
        except:
            text = None
        return text or None

