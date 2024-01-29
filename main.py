import utils.components.controller as controller
from utils.components import text_generator as tg, text_to_speech as tts, json_reader as js, video_downloader as vd, video_processing as vp, effects as ef

tg = tg.TextGenerator()
ef = ef.Effects()
tts = tts.TextToSpeech()
js = js.JsonReader()
vd = vd.VideoDownloader()
vp = vp.VideoProcessing(ef)

controller = controller.Controller(vd, vp, tg, tts, js)

if __name__ == '__main__':
    controller.run()
