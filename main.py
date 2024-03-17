import components.controller as controller
from components import json_reader as js, text_generator as tg, text_to_speech as tts, video_downloader as vd, \
    effects as ef, video_processing as vp

tg = tg.TextGenerator()
ef = ef.Effects()
tts = tts.TextToSpeech()
js = js.JsonReader()
vd = vd.VideoDownloader()
vp = vp.VideoProcessing(ef)

controller = controller.Controller(vd, vp, tg, tts, js)

if __name__ == '__main__':
    controller.run()