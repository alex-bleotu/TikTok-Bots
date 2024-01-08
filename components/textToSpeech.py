from google.cloud import speech
from google.cloud import texttospeech
import os

def generate():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "utils/credentials.json"

    tts_client = texttospeech.TextToSpeechClient()

    with open("temp/text.txt", 'r') as file:
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
    if not os.path.exists("temp/text.mp3"):
        open("temp/text.mp3", 'w').close()
    with open("temp/text.mp3", "wb") as out:
        out.write(response.audio_content)

    os.remove("temp/text.txt")



