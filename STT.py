import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the microphone as the audio source
with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")
    audio = recognizer.listen(source)

try:
    # Recognize speech using Google Web Speech API
    print("Recognizing...")
    text = recognizer.recognize_google(audio)
    print("You said: " + text)
except sr.UnknownValueError:
    print("Google Web Speech API could not understand the audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Web Speech API; {e}")
