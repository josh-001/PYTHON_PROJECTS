import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use microphone as source
while True:
    with sr.Microphone() as source:
        print("🎙️ Speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        # text = recognizer.recognize_google(audio)
        # print("📝 You said: " + text)
        # text = recognizer.recognize_google(audio)
        # print("📝 You said: " + text)
    try:
        print("🧠 Recognizing...")
        text = recognizer.recognize_google(audio)
        print("📝 You said: " + text)
        # Convert speech to text using Google Web Speech API
        
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
    except sr.RequestError as e:
        print(f"⚠️ Could not request results; {e}")
