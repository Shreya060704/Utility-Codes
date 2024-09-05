from gtts import gTTS
import os

def text_to_speech(text, language='en', filename='output.mp3'):
    # Initialize gTTS with the given text and language
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the audio file
    tts.save(filename)
    print(f"Audio saved as {filename}")

    # Optionally, play the audio file (works on some systems)
    os.system(f"start {filename}")  # For Windows
    # os.system(f"xdg-open {filename}")  # For Linux
    # os.system(f"open {filename}")  # For macOS

def main():
    # Define the text to be converted to speech
    text = """
    Hello, and welcome to this demo of the text-to-speech application. 
    Today, we will show you how text can be converted into spoken words using Python. 
    This demonstration highlights the power and versatility of text-to-speech technology, 
    which can be used for a variety of applications such as creating audiobooks, 
    assisting with accessibility needs, and enhancing interactive experiences.
    We hope you find this demo informative and enjoyable. Thank you for listening.
    """
    
    # Define language and filename
    language = 'en'
    filename = 'demo_speech.mp3'
    
    text_to_speech(text, language, filename)

if __name__ == "__main__":
    main()
