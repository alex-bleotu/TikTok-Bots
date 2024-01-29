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

def string_to_seconds(time):
    time = time.split(':')
    return int(time[0]) * 60 + int(time[1])


class MotivationalVideo:
    def __init__(self, type, url, filtered, music, start, end):
        self.type = VideoType.from_str(type)
        self.url = url
        self.filtered = filtered
        self.music = music
        self.start = string_to_seconds(start)
        self.end = string_to_seconds(end)


class FactVideo:
    def __init__(self, type, topic, voice, background, example):
        self.type = VideoType.from_str(type)
        self.topic = topic
        self.voice = voice
        self.background = background
        self.example = example

class StoryVideo:
    def __init__(self, type, topic, voice, background, example):
        self.type = VideoType.from_str(type)
        self.topic = topic
        self.voice = voice
        self.background = background
        self.example = example


class CaptionSettings:
    def __init__(self, fontSize, color, font, strokeColor, strokeWidth, align, position, enabled, bgColor, kerning, interline, phrase):
        self.fontSize = fontSize
        self.color = color
        self.font = font
        self.strokeColor = strokeColor
        self.strokeWidth = strokeWidth
        self.align = align
        self.position = position
        self.enabled = enabled
        self.bgColor = bgColor
        self.kerning = kerning
        self.interline = interline
        self.phrase = phrase


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
            elif video_type == VideoType.STORY:
                return StoryVideo(**data)
            else:
                raise ValueError("Invalid user type")

    def create_caption_settings_from_json(self):
        with open("caption.json", 'r') as file:
            data = json.load(file)
            return CaptionSettings(**data)
