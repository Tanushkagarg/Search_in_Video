from pytube import YouTube
from moviepy.editor import *

def extract_audio_from_link(video_link):
    yt = YouTube(video_link)
    video_stream = yt.streams.filter(file_extension='mp4').first()
    video_file = video_stream.download(filename='temp_video')
    video = VideoFileClip(video_file)
    audio = video.audio
    audio_file = "extracted_audio.wav" 
    audio.write_audiofile(audio_file)
    audio.close()
    video.close()
    os.remove(video_file)
    
video_link=input("Enter the Video Link : ")
extract_audio_from_link(video_link)
