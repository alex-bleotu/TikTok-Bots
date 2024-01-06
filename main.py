from components import textToSpeech as tts
from components import videoProcessing as vid
from components import textGenerator as tg
from components.textGenerator import Type

tg.generate(Type.FACTS)
tts.generate()
vid.generate("output")
