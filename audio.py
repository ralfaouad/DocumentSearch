# pip3 install SpeechRecognition pydub
import speech_recognition as sr

def speech2text():
    # initialize the recognizer
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        return text

# from spellchecker import SpellChecker

# spell = SpellChecker()

# find those words that may be misspelled
# misspelled = spell.unknown(['something', 'is', 'hapenning', 'here'])

# for word in misspelled:
#     # Get the one `most likely` answer
#     print(spell.correction(word))

# find those words that may be misspelled
# misspelled = spell.unknown(['artifial', 'us', 'wlak','on','the','grou'])

# for word in misspelled:
#     # Get the one `most likely` answer
#     print(spell.correction(word))

