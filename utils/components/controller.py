from utils.components.json_reader import VideoType as Type

banner = """
  ____  _                _         ____        _   
 / ___|| |__   ___  _ __| |_ ___  | __ )  ___ | |_ 
 \___ \|  _ \ / _ \|  __| __/ __| |  _ \ / _ \| __|
  ___) | | | | (_) | |  | |_\__ \ | |_) | (_) | |_ 
 |____/|_| |_|\___/|_|   \__|___/ |____/ \___/ \__|
                                                   
"""


class Controller:
    def __init__(self, vd, vp, tg, tts, js):
        self.__vd = vd
        self.__vp = vp
        self.__tg = tg
        self.__tts = tts
        self.__js = js

    def __runMotivation(self, video, caption):
        print("Downloading video from " + video.url)
        # self.__vd.download(video.url)
        print("Video downloaded")
        self.__vp.generate_motivational(caption, video.start, video.end, video.filtered)
        print("Video generated")
        # self.__vp.open_video()

    def __runFacts(self, video, caption):
        script = self.__tg.generate(Type.FACT, video.topic)
        print("Script generated about " + video.topic)
        print(script)
        self.__tg.save_text(script)
        self.__tts.generate(video.voice)
        print("TTS generated")
        self.__vp.generate_facts(caption)
        print("Video generated")
        # self.__vp.open_video()

    def run(self):
        print(banner + "\n")

        video = self.__js.create_user_from_json()
        caption = self.__js.create_caption_settings_from_json()
        if video.type == Type.MOTIVATION:
            self.__runMotivation(video, caption)
        elif video.type == Type.FACT:
            self.__runFacts(video, caption)
        else:
            raise Exception("Invalid video type")
