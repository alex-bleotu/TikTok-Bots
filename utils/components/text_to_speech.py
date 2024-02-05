from elevenlabs import generate, set_api_key
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ.get('TOKEN_ELEVENLABS')

class TextToSpeech:
    def __init__(self):
        set_api_key(key)
        pass

    def generate(self, voice="Adam"):
        with open("utils/temp/text.txt", 'r') as file:
            text = file.read().replace('\n', '')

        audio = generate(
            text,
            voice=voice,
            model="eleven_multilingual_v2"
        )

        if not os.path.exists("utils/temp/audio.mp3"):
            open("utils/temp/audio.mp3", 'w').close()
        with open("utils/temp/audio.mp3", "wb") as out:
            out.write(audio)

        os.remove("utils/temp/text.txt")
