from utils.components.json_reader import VideoType as Type

class Controller:
    def __init__(self, vd, vp, tg, tts, js):
        self.__vd = vd
        self.__vp = vp
        self.__tg = tg
        self.__tts = tts
        self.__js = js

    def __runMotivation(self, video):
        self.__vd.download(video.url)
        self.__vp.generate_facts()
        # self.__vp.open_video()

    def __runFacts(self, video):
        script = self.__tg.generate(Type.FACT, video.topic)
        print("Script generated about " + video.topic)
        print(script)
        self.__tg.save_text(script)
        self.__tts.generate(video.voice)
        print("TTS generated")
        self.__vp.generate_facts(video.caption)
        print("Video generated")
        # self.__vp.open_video()

    def run(self):
        print("YouTube Short Video Generator\n")

        video = self.__js.create_user_from_json()
        if video.type == Type.MOTIVATION:
            self.__runMotivation(video)
        elif video.type == Type.FACT:
            self.__runFacts(video)
        else:
            raise Exception("Invalid video type")
