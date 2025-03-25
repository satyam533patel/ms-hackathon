import azure.cognitiveservices.speech as speechsdk

# Azure Speech API credentials
SPEECH_KEY = "Fj1KPt7grC6bAkNja7daZUstpP8wZTXsV6Zjr2FOxkO7wsBQ5SzQJQQJ99BCACHYHv6XJ3w3AAAAACOGL3Xg"
SPEECH_REGION = "eastus2"

def recognize_from_microphone():
    """Recognizes speech and returns text from the microphone."""
    try:
        # Configure Azure Speech Service
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
        speech_config.speech_recognition_language = "en-US"

        # ✅ Correct way to initialize AudioConfig (Default Microphone)
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        # Initialize the speech recognizer
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print("Listening...")
        result = recognizer.recognize_once_async().get()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech detected."
        elif result.reason == speechsdk.ResultReason.Canceled:
            return "Speech recognition canceled."
    except Exception as e:
        return f"Error: {str(e)}"
