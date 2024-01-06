from google.cloud import speech
from google.cloud import texttospeech
import os

def generate(fileName):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "utils/credentials.json"

    tts_client = texttospeech.TextToSpeechClient()

    with open("texts/" + fileName + ".txt", 'r') as file:
        text = file.read().replace('\n', '')
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-Q",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1

    )
    response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    if not os.path.exists("audio/" + fileName + ".mp3"):
        open("audio/" + fileName + ".mp3", 'w').close()
    with open("audio/" + fileName + ".mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file '" + fileName + ".mp3'")

