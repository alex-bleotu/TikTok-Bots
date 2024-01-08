import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from mutagen.mp3 import MP3
import pvleopard
from moviepy.config import change_settings
from moviepy.video.fx import all as fx

change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


class VideoProcessing:
    def __init__(self):
        pass

    def __choose_random_video(self, folder_path):
        videos = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov'))]
        return random.choice(videos) if videos else None

    def __get_audio_duration(self, audio_file):
        audio = MP3(audio_file)
        return audio.info.length

    def __process_video(self, video_path, audio_path, output_path, caption, start = None, end = None, filtered = False):
        audio_duration = self.__get_audio_duration(audio_path)
        video_clip = VideoFileClip(video_path)

        if start != None and end != None:
            max_start = max(0, video_clip.duration - audio_duration)
            start_time = random.uniform(0, max_start)
            video_segment = video_clip.subclip(start_time, start_time + audio_duration)
        else:
            video_segment = video_clip.subclip(start, end)

        if filtered:
            video_segment = video_segment.fx(fx.blackwhite)

        new_width = int(video_segment.size[1] * 9 / 16)
        margin = (video_segment.size[0] - new_width) // 2
        cropped_clip = video_segment.crop(x1=margin, x2=video_segment.size[0] - margin)

        audio_clip = AudioFileClip(audio_path).volumex(0.5)
        final_clip = cropped_clip.set_audio(audio_clip)

        if caption.enabled == True:
            final_clip = self.__add_subtitles(final_clip, audio_path, caption)

        final_clip.write_videofile(output_path, codec='libx264', logger=None)

        video_clip.close()
        video_segment.close()
        cropped_clip.close()
        audio_clip.close()
        final_clip.close()

    def __transcribe_audio(self, audio_path):
        options = pvleopard.create(
            access_key="cif3dRAtaqTdDpe90VZJ6p7Kd25T+zM2ReMnkLP0+VgAwh1NxbEzHA=="
        )

        transcript, words = options.process_file(audio_path)

        return words

    def __add_subtitles(self, video_clip, audio_path, caption):
        transcription_result = self.__transcribe_audio(audio_path)

        subtitles_clips = []

        for phrase in transcription_result:
            start_time = phrase.start_sec
            end_time = phrase.end_sec
            text = phrase.word

            txt_clip = TextClip(text.upper(),
                                fontsize=caption.fontSize,
                                color=caption.color,
                                font=caption.font,
                                stroke_color=caption.strokeColor,
                                stroke_width=caption.strokeWidth,
                                align=caption.align,
                                kerning=caption.kerning,
                                interline=caption.interline,
                                bg_color=caption.bgColor,
                                method="caption"
            ).set_position(caption.position).set_duration(
                end_time - start_time).set_start(start_time)

            subtitles_clips.append(txt_clip)

        final_clip = CompositeVideoClip([video_clip] + subtitles_clips)

        return final_clip

    def generate_motivational(self, caption, start, end, filtered):
        video_file = 'utils/temp/video.mp4'
        output_file = 'utils/output/output.mp4'
        audio_file = 'utils/temp/audio.mp3'

        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio.subclip(start, end)
        audio_clip.write_audiofile(audio_file, logger=None)
        video_clip.close()

        self.__process_video(video_file, audio_file, output_file, caption, start, end, filtered)

        os.remove(audio_file)
        os.remove(video_file)

    def generate_facts(self, caption, filtered):
        video_folder = 'utils/background'
        audio_file = 'utils/temp/text.mp3'
        output_file = 'utils/output/output.mp4'

        random_video = self.__choose_random_video(video_folder)
        if random_video:
            self.__process_video(os.path.join(video_folder, random_video), audio_file, output_file, caption)

        os.remove(audio_file)

    def generate_motivation(self, subtitles = True):
        video_folder = 'util/temp'
        audio_file = 'util/temp/text.mp3'
        output_file = 'util/output/output.mp4'

    def open_video(self):
        os.startfile('util/output/output.mp4')