import json
from enum import Enum


class VideoType(Enum):
    FACT = "fact"
    MOTIVATION = "motivation"
    STORY = "story"

    @staticmethod
    def from_str(label):
        for name, member in VideoType.__members__.items():
            if member.value == label:
                return member
        raise ValueError(f"{label} is not a valid VideoType")


class MotivationalVideo:
    def __init__(self, type, url, caption, flitered, music):
        self.type = VideoType.from_str(type)
        self.url = url
        self.caption = caption
        self.flitered = flitered
        self.music = music


class FactVideo:
    def __init__(self, type, topic, caption, voice):
        self.type = VideoType.from_str(type)
        self.topic = topic
        self.caption = caption
        self.voice = voice


class JsonReader:
    def __init__(self):
        pass

    def create_user_from_json(self):
        with open("video.json", 'r') as file:
            data = json.load(file)
            video_type = VideoType.from_str(data['type'])

            if video_type == VideoType.MOTIVATION:
                return MotivationalVideo(**data)
            elif video_type == VideoType.FACT:
                return FactVideo(**data)
            else:
                raise ValueError("Invalid user type")
