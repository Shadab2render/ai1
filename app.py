import os
from datetime import datetime
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load env vars locally (Render uses its own secure UI)
load_dotenv()

# === 🔐 Azure Keys from environment ===
AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION")

if not AZURE_KEY or not AZURE_REGION:
    print("❌ Azure Speech credentials not set.")
    exit(1)

# === 🗃️ Create transcripts folder if needed ===
os.makedirs("transcripts", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"transcripts/meeting_{timestamp}.txt"

# === 🎙️ Speech setup ===
speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
speech_config.speech_recognition_language = "en-IN"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

def save_to_file(text):
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def handle_result(evt):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("📝", evt.result.text)
        save_to_file(evt.result.text)

print("🎤 Listening... Press Ctrl+C to stop.")
speech_recognizer.recognized.connect(handle_result)
speech_recognizer.start_continuous_recognition()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("🛑 Stopped.")
    speech_recognizer.stop_continuous_recognition()
    print(f"📁 Transcript saved to {output_file}")
