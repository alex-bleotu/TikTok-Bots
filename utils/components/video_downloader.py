from pytube import YouTube
from moviepy.editor import *
import os


class VideoDownloader:
    def __init__(self):
        pass

    def download(url):
        print("Downloading video from YouTube...")
        yt = YouTube(url)
        ys = yt.streams.get_highest_resolution()
        ys.download(output_path="temp", filename="video.mp4")
        print("Downloaded video complete!")

    def  download_high_quality(url):
        save_path = "temp"

        print("Downloading video from YouTube...")
        yt = YouTube(url)

        ys = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        ys_audio = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        video_filename = ys.download(output_path=save_path)
        audio_filename = ys_audio.download(output_path=save_path)

        video_path = os.path.join(save_path, video_filename)
        audio_path = os.path.join(save_path, audio_filename)

        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)

        final_clip = video_clip.set_audio(audio_clip)

        final_path = os.path.join(save_path, "video.mp4")

        final_clip.write_videofile(final_path, logger=None)

        os.remove(video_path)
        os.remove(audio_path)

        print("Downloading video completed!")