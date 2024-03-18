import os
import random
import subprocess
from mutagen.mp3 import MP3
from moviepy.config import change_settings
import whisper_timestamped
from components.json_reader import FontSize
from moviepy.editor import (VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip,
                            concatenate_videoclips, clips_array)

change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})
change_settings({"FFMPEG_BINARY": "C:\Program Files\\ffmpeg\\bin\\ffmpeg.exe"})

class VideoProcessing:
    def __init__(self, effects):
        self.__effects = effects
        self.__music_path = "utils/music/" # .mp3 / .wav
        self.__background_path = "utils/background/" # .mp4 / .avi / .mov
        self.__audio_path = "utils/temp/audio.mp3"
        self.__output_path = "output/output.mp4"
        self.__temp_output_path = "utils/temp/output/"
        self.__video_path = "utils/temp/video.mp4"
        pass

    def __crop_to_aspect_ratio(clip, aspect_ratio=9 / 16):
        target_height = clip.h
        target_width = int(target_height * aspect_ratio)
        if target_width > clip.w:
            target_width = clip.w
            target_height = int(target_width / aspect_ratio)

        x_center = (clip.w - target_width) // 2
        y_center = (clip.h - target_height) // 2

        return clip.crop(x1=x_center, y1=y_center, width=target_width, height=target_height)

    def __choose_random_video(self, background):
        videos = [f for f in os.listdir(self.__background_path + background) if f.endswith(('.mp4', '.avi', '.mov'))]
        return random.choice(videos) if videos else None

    def __get_audio_duration(self, audio_file):
        audio = MP3(audio_file)
        return audio.info.length

    def __add_music(self, video_clip, type):
        music_folder = self.__music_path + type + "/"

        music_files = [file for file in os.listdir(music_folder) if file.endswith(('.mp3', '.wav'))]
        selected_music_file = random.choice(music_files)
        music_clip = AudioFileClip(os.path.join(music_folder, selected_music_file))
        start_point = random.uniform(10, max(0, music_clip.duration - video_clip.duration))
        music_clip = music_clip.volumex(0.1)
        music_clip = music_clip.subclip(start_point, start_point + video_clip.duration)
        composite_audio_clip = CompositeAudioClip([video_clip.audio, music_clip.set_start(0)])
        return video_clip.set_audio(composite_audio_clip)

    def __process_video(self, video_path, caption, start=None, end=None, filtered=False,
                        chain=False, index=0, music=None, default_audio=False, custom_video=False, position=None):
        if default_audio == False:
            audio_duration = self.__get_audio_duration(self.__audio_path)

        video_clip = VideoFileClip(video_path)

        if start == None and end == None:
            max_start = max(0, video_clip.duration - audio_duration)
            start_time = random.uniform(0, max_start)
            video_segment = video_clip.subclip(start_time, start_time + audio_duration)
        elif custom_video:
            max_start = max(0, video_clip.duration - (end - start))
            start_time = random.uniform(0, max_start)
            video_segment = video_clip.subclip(start_time, start_time+ end - start)
        else:
            video_segment = video_clip.subclip(start, end)

        if filtered != False:
            video = self.__effects.add_effects(video_segment, filtered)
        else:
            video = video_segment

        if custom_video == True:
            custom_clip = VideoFileClip(self.__video_path)
            custom_clip = custom_clip.subclip(start, end)
            custom_clip = custom_clip.resize((1280, 720))
            custom_clip = custom_clip.crop(x1=235, x2=1045)
            custom_clip = custom_clip.set_position(("center", 0))

            background_video = video.crop(x1=235, x2=1045)
            background_video = background_video.resize((810, 640))
            background_video = background_video.without_audio()
            background_video = background_video.set_position(("center", 720))

            cropped_clip = clips_array([[custom_clip], [background_video]])

            custom_clip.close()
        else:
            new_width = int(video.size[1] * 9 / 16)
            margin = (video.size[0] - new_width) // 2
            cropped_clip = video.crop(x1=margin, x2=video.size[0] - margin)

        if default_audio == False:
            audio_clip = AudioFileClip(self.__audio_path).volumex(1)
            final_clip = cropped_clip.set_audio(audio_clip)
        else:
            audio = cropped_clip.audio
            audio.write_audiofile(self.__audio_path, logger=None, fps=44100)
            audio.close()
            # command = f"ffmpeg -i \"{self.__video_path}\" -vn -ab 128k -ar 44100 -y \"{self.__audio_path}\""
            # subprocess.call(command, shell=True)
            final_clip = cropped_clip

        if caption.enabled == True:
            final_clip = self.__add_subtitles(final_clip, caption)

        if chain == False:
            if music != None:
                final_clip = self.__add_music(final_clip, music)
            final_clip.write_videofile(self.__output_path, codec='libx264', logger=None)
        else:
            final_clip.write_videofile(self.__temp_output_path + str(index) + ".mp4", codec='libx264', logger=None)

        video_clip.close()
        video_segment.close()
        cropped_clip.close()
        final_clip.close()

    def __transcribe_audio(self, audio_path):
        model = whisper_timestamped.load_model("base")
        caption = whisper_timestamped.transcribe(model, audio_path, "en", min_word_duration=0.01)
        return caption

    def __split_into_chunks(self, words, max_chars=20):
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_length = len(word['text']) + 1
            if current_length + word_length > max_chars and current_chunk:
                chunks.append({
                    'text': ' '.join([w['text'] for w in current_chunk]),
                    'start': current_chunk[0]['start'],
                    'end': current_chunk[-1]['end']
                })
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        if current_chunk:
            chunks.append({
                'text': ' '.join([w['text'] for w in current_chunk]),
                'start': current_chunk[0]['start'],
                'end': current_chunk[-1]['end']
            })

        return chunks

    def __remove_punctuation(self, text):
        return text.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace(":", "").replace(";",
                                                                                                                 "").replace(
            "-", "").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace("{", "").replace("}",
                                                                                                                  "").replace(
            "'", "").replace('"', "")

    def __add_subtitles(self, video_clip, caption):
        width = video_clip.size[0]
        captionSize = width / 15
        if caption.font_size == FontSize.SMALL:
            captionSize *= 0.5
        elif caption.font_size == FontSize.MEDIUM:
            captionSize *= 1
        elif caption.font_size == FontSize.LARGE:
            captionSize *= 1.5

        transcription_result = self.__transcribe_audio(self.__audio_path)

        subtitles_clips = []

        if caption.title:
            text = transcription_result["segments"][0]["text"].strip()
            if not caption.punctuation:
                text = self.__remove_punctuation(text).upper()

            split_index = text.find("TO") + 3
            first_text = text[:split_index].strip()
            first_text = first_text.replace("THREE", "3")
            second_text = text[split_index:].strip()

            start_time = 0
            end_time = transcription_result["segments"][0]["end"]

            first = TextClip(first_text,
                             fontsize=captionSize,
                             color=caption.color,
                             font=caption.font,
                             stroke_color=caption.stroke_color,
                             stroke_width=caption.stroke_width,
                             align=caption.align,
                             kerning=caption.kerning,
                             interline=caption.interline,
                             bg_color=caption.bgColor,
                             method="caption", size=(550, 50)
                             ).set_position(caption.position).set_duration(
                end_time - start_time).set_start(start_time)

            second = TextClip(second_text,
                              fontsize=captionSize,
                              color="yellow",
                              font=caption.font,
                              stroke_color=caption.stroke_color,
                              stroke_width=caption.stroke_width,
                              align=caption.align,
                              kerning=caption.kerning,
                              interline=caption.interline,
                              bg_color=caption.bgColor,
                              method="caption", size=(550, 150)
                              ).set_position(caption.position).set_duration(
                end_time - start_time).set_start(start_time)

            first = first.set_position(("center", 25))
            if len(second_text) > 20:
                second = second.set_position(("center", 65))
            else:
                second = second.set_position(("center", 35))

            background_clip = ColorClip(size=(first.size[0] + 100, first.size[1] + second.size[1] + 10), color=(0, 0,
                                                                                                                0, 0))
            final_clip = CompositeVideoClip([background_clip, first, second],
                                            size=background_clip.size).set_duration(
                end_time - start_time + 1).set_start(
                start_time).set_position(("center", "center"))

            subtitles_clips.append(final_clip)

            transcription_result["segments"].pop(0)

        for phrase in transcription_result["segments"]:
            if caption.phrase:
                words = phrase["words"]

                parts = self.__split_into_chunks(words)

                for part in parts:
                    text = part["text"].strip()
                    start_time = part["start"]
                    end_time = part["end"]

                    if not caption.punctuation:
                        text = self.__remove_punctuation(text)

                    txt_clip = TextClip(text.replace("Lose", "Lois"),
                                        fontsize=captionSize,
                                        color=caption.color,
                                        font=caption.font,
                                        stroke_color=caption.stroke_color,
                                        stroke_width=caption.stroke_width,
                                        align=caption.align,
                                        kerning=caption.kerning,
                                        interline=caption.interline,
                                        bg_color=caption.bgColor,
                                        # method="caption"
                                        ).set_position(caption.position).set_duration(
                        end_time - start_time).set_start(start_time)

                    subtitles_clips.append(txt_clip)
            else:
                for word in phrase["words"]:
                    text = word["text"].strip()
                    start_time = word["start"]
                    end_time = word["end"]

                    if not caption.punctuation:
                        text = self.__remove_punctuation(text)

                    txt_clip = TextClip(text.replace("Lose", "Lois"),
                                        fontsize=captionSize,
                                        color=caption.color,
                                        font=caption.font,
                                        stroke_color=caption.stroke_color,
                                        stroke_width=caption.stroke_width,
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

    def generate_motivational(self, video, caption, index):
        video_clip = VideoFileClip(self.__video_path)
        audio_clip = video_clip.audio.subclip(video.start, video.end)
        audio_clip.write_audiofile(self.__audio_path, logger=None)
        video_clip.close()
        self.__process_video(self.__video_path, caption, video.start, video.end, video.filtered, chain=True,
                             index=index)
        os.remove(self.__audio_path)
        os.remove(self.__video_path)

    def generate_facts(self, video, caption):
        random_video = self.__choose_random_video(video.background)
        if random_video:
            self.__process_video(os.path.join(self.__background_path + video.background, random_video),
                                 caption, filtered=video.filtered, music=video.music)
        os.remove(self.__audio_path)

    def generate_segments(self, video, caption):
        videoLength = (video.end[0] - video.start[0]) / video.segments
        for index in range(0, video.segments):
            random_video = self.__choose_random_video(video.background)
            if random_video:
                video_clip = VideoFileClip(os.path.join(self.__background_path + video.background, random_video))
                self.__process_video(os.path.join(self.__background_path + video.background, random_video),
                                     caption, start=index * videoLength, end=(index + 1) * videoLength, chain=True,
                                     index=index, default_audio=True, custom_video=True, position=video.position)
                video_clip.close()
        self.__move_output()
        os.remove(self.__audio_path)
        os.remove(self.__video_path)

    def generate_stories(self, video, caption):
        random_video = self.__choose_random_video(video.background)
        if random_video:
            self.__process_video(os.path.join(self.__background_path + video.background, random_video), caption, music=video.music)
        os.remove(self.__audio_path)

    def compile_video(self, video):
        videos = []
        for file in os.listdir(self.__temp_output_path):
            videos.append(VideoFileClip(self.__temp_output_path + file))

        final_clip = concatenate_videoclips(videos)
        if video.music != None:
            final_clip = self.__add_music(final_clip, video.music)
        final_clip.write_videofile(self.__output_path, codec='libx264', logger=None)

        for file in os.listdir(self.__temp_output_path):
            os.remove(self.__temp_output_path + file)

    def __move_output(self):
        files = os.listdir(self.__temp_output_path)
        for file in files:
            if os.path.exists("output/" + file):
                os.remove("output/" + file)
            os.rename(self.__temp_output_path + file, "output/" + file)
