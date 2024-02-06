import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip
import moviepy.editor as mp
from mutagen.mp3 import MP3
from moviepy.config import change_settings
import whisper_timestamped

change_settings({"IMAGEMAGICK_BINARY": "C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"})


class VideoProcessing:
    def __init__(self, effects):
        self.__effects = effects
        pass

    def __choose_random_video(self, background):
        videos = [f for f in os.listdir("utils/background/" + background) if f.endswith(('.mp4', '.avi', '.mov'))]
        return random.choice(videos) if videos else None

    def __get_audio_duration(self, audio_file):
        audio = MP3(audio_file)
        return audio.info.length

    def __add_music(self, video_clip, type):
        music_folder = "utils/music/" + type + "/"

        music_files = [file for file in os.listdir(music_folder) if file.endswith(('.mp3', '.wav'))]
        selected_music_file = random.choice(music_files)
        music_clip = AudioFileClip(os.path.join(music_folder, selected_music_file))
        start_point = random.uniform(10, max(0, music_clip.duration - video_clip.duration))
        music_clip = music_clip.volumex(0.1)
        music_clip = music_clip.subclip(start_point, start_point + video_clip.duration)
        composite_audio_clip = CompositeAudioClip([video_clip.audio, music_clip.set_start(0)])
        return video_clip.set_audio(composite_audio_clip)

    def __process_video(self, video_path, audio_path, output_path, caption, start=None, end=None, filtered=False,
                        chain=False, index=0, music=None):
        audio_duration = self.__get_audio_duration(audio_path)
        video_clip = VideoFileClip(video_path)

        if start == None and end == None:
            max_start = max(0, video_clip.duration - audio_duration)
            start_time = random.uniform(0, max_start)
            video_segment = video_clip.subclip(start_time, start_time + audio_duration)
        else:
            video_segment = video_clip.subclip(start, end)

        if filtered != False:
            video = self.__effects.add_effects(video_segment, filtered)
        else:
            video = video_segment

        new_width = int(video.size[1] * 9 / 16)
        margin = (video.size[0] - new_width) // 2
        cropped_clip = video.crop(x1=margin, x2=video.size[0] - margin)

        audio_clip = AudioFileClip(audio_path).volumex(1)
        final_clip = cropped_clip.set_audio(audio_clip)

        if caption.enabled == True:
            final_clip = self.__add_subtitles(final_clip, audio_path, caption)

        # final_clip.preview()
        if chain == False:
            if music != None:
                final_clip = self.__add_music(final_clip, music)
            final_clip.write_videofile(output_path, codec='libx264', logger=None)
        else:
            final_clip.write_videofile("utils/temp/output/" + str(index) + ".mp4", codec='libx264', logger=None)

        video_clip.close()
        video_segment.close()
        cropped_clip.close()
        final_clip.close()
        audio_clip.close()

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

    def __add_subtitles(self, video_clip, audio_path, caption):
        transcription_result = self.__transcribe_audio(audio_path)

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
                             fontsize=caption.font_size - 5,
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
                              fontsize=caption.font_size - 5,
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

            # print(second_text)
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

                    txt_clip = TextClip(text.upper(),
                                        fontsize=caption.font_size,
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

                    txt_clip = TextClip(text.upper(),
                                        fontsize=caption.font_size,
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

    def generate_motivational(self, caption, start, end, filtered, index):
        video_file = 'utils/temp/video.mp4'
        output_file = 'output/output.mp4'
        audio_file = 'utils/temp/audio.mp3'

        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio.subclip(start, end)
        audio_clip.write_audiofile(audio_file, logger=None)
        video_clip.close()

        self.__process_video(video_file, audio_file, output_file, caption, start, end, filtered, chain=True,
                             index=index)

        os.remove(audio_file)
        os.remove(video_file)

    def generate_facts(self, caption, background, filtered=None, music=None):
        audio_file = 'utils/temp/audio.mp3'
        output_file = 'output/output.mp4'

        random_video = self.__choose_random_video(background)
        if random_video:
            self.__process_video(os.path.join("utils/background/" + background, random_video), audio_file, output_file,
                                 caption, filtered=filtered, music=music)

        # os.remove(audio_file)

    def generate_stories(self, caption, background, music = None):
        audio_file = 'utils/temp/audio.mp3'
        output_file = 'output/output.mp4'

        random_video = self.__choose_random_video(background)
        if random_video:
            self.__process_video(os.path.join("utils/background/" + background, random_video), audio_file,
                                 output_file, caption, music=music)

        os.remove(audio_file)

    def open_video(self):
        os.startfile('output/output.mp4')

    def compile_video(self, music=None):
        temp_output_file = 'utils/temp/output/'
        output_file = 'output/output.mp4'

        # get all videos from temp_output and merge them
        videos = []
        for file in os.listdir(temp_output_file):
            videos.append(VideoFileClip(temp_output_file + file))

        final_clip = mp.concatenate_videoclips(videos)
        if music != None:
            final_clip = self.__add_music(final_clip, music)
        final_clip.write_videofile(output_file, codec='libx264', logger=None)

        for file in os.listdir(temp_output_file):
            os.remove(temp_output_file + file)
