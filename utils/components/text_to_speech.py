from elevenlabs import generate, set_api_key
import elevenlabs
import os


class TextToSpeech:
    def __init__(self):
        set_api_key("42474569d82f15cae512b010c2332508")
        pass

    def generate(self, voice="Adam"):
        with open("utils/temp/text.txt", 'r') as file:
            text = file.read().replace('\n', '')

        audio = generate(
            text,
            voice=voice,
            model="eleven_multilingual_v2"
        )

        if not os.path.exists("utils/temp/text.mp3"):
            open("utils/temp/text.mp3", 'w').close()
        with open("utils/temp/text.mp3", "wb") as out:
            out.write(audio)

        os.remove("utils/temp/text.txt")
