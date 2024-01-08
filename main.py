import utils.components.controller as controller
from utils.components import text_generator as tg, text_to_speech as tts, json_reader as js, video_downloader as vd, video_processing as vp

tg = tg.TextGenerator()
tts = tts.TextToSpeech()
js = js.JsonReader()
vd = vd.VideoDownloader()
vp = vp.VideoProcessing()

controller = controller.Controller(vd, vp, tg, tts, js)

if __name__ == '__main__':
    controller.run()