from moviepy.video.fx import all as fx


class Effects:
    def __init__(self):
        pass

    def __dark_frame(self, frame):
        return frame * 0.5

    def __very_dark_frame(self, frame):
        return frame * 0.25

    def __blackwhite(self, video):
        return video.fx(fx.blackwhite)

    def add_effects(self, video, effects):
        if "blackwhite" in effects:
            video = self.__blackwhite(video)
        if "dark" in effects:
            video = video.fl_image(self.__dark_frame)
        if "very_dark" in effects:
            video = video.fl_image(self.__very_dark_frame)
        return video