from google.cloud import texttospeech
import os


class TextToSpeech:
    def __init__(self):
        pass

    def generate(self, voice="default"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "utils/credentials/credentials.json"

        tts_client = texttospeech.TextToSpeechClient()

        with open("utils/temp/text.txt", 'r') as file:
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
        if not os.path.exists("utils/temp/text.mp3"):
            open("utils/temp/text.mp3", 'w').close()
        with open("utils/temp/text.mp3", "wb") as out:
            out.write(response.audio_content)

        os.remove("utils/temp/text.txt")
