# pip3 install SpeechRecognition pydub
import speech_recognition as sr

# In this file: Speech to Text

def speech2text():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        text = r.recognize_google(audio_data)
        return text

