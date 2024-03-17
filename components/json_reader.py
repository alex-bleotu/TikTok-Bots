import json
from enum import Enum


class VideoType(Enum):
    FACT = "fact"
    MOTIVATION = "motivation"
    STORY = "story"
    SEGMENT = "segment"

    @staticmethod
    def from_str(label):
        for name, member in VideoType.__members__.items():
            if member.value == label:
                return member
        raise ValueError(f"{label} is not a valid VideoType")

class StoryType(Enum):
    CREEPY = "creepy"
    QUESTION = "question"
    JOKE = "joke"
    STORY = "story"

    @staticmethod
    def from_str(label):
        for name, member in StoryType.__members__.items():
            if member.value == label:
                return member
        raise ValueError(f"{label} is not a valid StoryType")

class FactType(Enum):
    FUNNY = "funny"
    INTERESTING = "interesting"
    SCARY = "scary"
    MOTIVATIONAL = "motivational"

    @staticmethod
    def from_str(label):
        for name, member in FactType.__members__.items():
            if member.value == label:
                return member
        raise ValueError(f"{label} is not a valid FactType")

class Position(Enum):
    TOP = "top"
    BOTTOM = "bottom"

    @staticmethod
    def from_str(label):
        for name, member in Position.__members__.items():
            if member.value == label:
                return member
        raise ValueError(f"{label} is not a valid Position")


class FontSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

    @staticmethod
    def from_str(label):
        for name, member in FontSize.__members__.items():
            if member.value == label:
                return member
        raise ValueError(f"{label} is not a valid FontSize")


def string_to_seconds(time_strings):
    result = []

    for time_str in time_strings:
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = minutes * 60 + seconds
        result.append(total_seconds)

    return result


class MotivationalVideo:
    def __init__(self, type, url, filtered, music, start, end):
        self.type = VideoType.from_str(type)
        self.url = url
        self.filtered = filtered
        self.music = music
        self.start = string_to_seconds(start)
        self.end = string_to_seconds(end)
        self.music = music


class FactVideo:
    def __init__(self, type, topic, voice, background, example, fact_type, filtered, music, test):
        self.type = VideoType.from_str(type)
        self.topic = topic
        self.voice = voice
        self.background = background
        self.example = example
        self.fact_type = FactType.from_str(fact_type)
        self.filtered = filtered
        self.music = music
        self.test = test


class StoryVideo:
    def __init__(self, type, topic, voice, background, example, parts, story_type, music, test):
        self.type = VideoType.from_str(type)
        self.topic = topic
        self.voice = voice
        self.background = background
        self.example = example
        self.parts = parts
        self.story_type = StoryType.from_str(story_type)
        self.music = music
        self.test = test

class SegmentsVideo:
    def __init__(self, type, url, start, end, background, position, segments):
        self.type = VideoType.from_str(type)
        self.url = url
        self.start = string_to_seconds(start)
        self.end = string_to_seconds(end)
        self.background = background
        self.position = Position.from_str(position)
        self.segments = segments


class CaptionSettings:
    def __init__(self, font_size, color, font, stroke_color, stroke_width, align, position, enabled, bg_color, kerning,
                 interline, phrase, punctuation, title):
        self.font_size = FontSize.from_str(font_size)
        self.color = color
        self.font = font
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width
        self.align = align
        self.position = position
        self.enabled = enabled
        self.bgColor = bg_color
        self.kerning = kerning
        self.interline = interline
        self.phrase = phrase
        self.punctuation = punctuation
        self.title = title


class JsonReader:
    def __init__(self):
        pass

    def create_video_from_json(self):
        with open("types/video.json", 'r') as file:
            data = json.load(file)
            video_type = VideoType.from_str(data['type'])

            if video_type == VideoType.MOTIVATION:
                return MotivationalVideo(**data)
            elif video_type == VideoType.FACT:
                return FactVideo(**data)
            elif video_type == VideoType.STORY:
                return StoryVideo(**data)
            elif video_type == VideoType.SEGMENT:
                return SegmentsVideo(**data)
            else:
                raise ValueError("Invalid user type")

    def create_caption_settings_from_json(self):
        with open("types/caption.json", 'r') as file:
            data = json.load(file)
            return CaptionSettings(**data)
