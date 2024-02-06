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

    def __run_motivation(self, video, caption):
        for index in range(0, len(video.url)):
            print("Downloading video from " + video.url[index])
            self.__vd.download(video.url[index])
            print("Video downloaded")
            self.__vp.generate_motivational(caption, video.start[index], video.end[index], video.filtered, index)
            print("Video " + str(index + 1) + " added\n")
            index += 1

        self.__vp.compile_video()

        print("Video generated")
        # self.__vp.open_video()

    def __run_facts(self, video, caption):
        script = self.__tg.generate(Type.FACT, video.topic, video.example, video.fact_type)
        if video.topic is not None:
            print("\nScript generated about " + video.topic)
        print("\nNew Script:\n" + script)
        self.__tg.save_text(script)
        self.__tts.generate(video.voice)
        print("\nTTS generated")
        self.__vp.generate_facts(caption, video.background, video.filtered)
        print("\nVideo generated")
        # self.__vp.open_video()

    def __run_story(self, video, caption):
        script = self.__tg.generate(Type.STORY, video.topic, video.example, video.story_type)
        if video.topic is not None:
            print("\nScript generated about " + video.topic)
        print("\n" + script)
        self.__tg.save_text(script)
        self.__tts.generate(video.voice)
        print("\nTTS generated")
        self.__vp.generate_stories(caption, video.background)
        print("\nVideo generated")
        # self.__vp.open_video()

    def run(self):
        print(banner + "\n")

        video = self.__js.create_video_from_json()
        caption = self.__js.create_caption_settings_from_json()
        if video.type == Type.MOTIVATION:
            self.__run_motivation(video, caption)
        elif video.type == Type.FACT:
            self.__run_facts(video, caption)
        elif video.type == Type.STORY:
            self.__run_story(video, caption)
        else:
            raise Exception("Invalid video type")
