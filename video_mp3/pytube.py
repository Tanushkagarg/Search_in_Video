import os
from pytube import YouTube

def download_audio(url):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        destination = '.' # Current directory

        out_file = video.download(output_path=destination)

        base, ext = os.path.splitext(out_file)
        new_file = base + '.wav'

        # Check if the file exists before attempting to rename it
        os.rename(out_file, new_file) 


        print(yt.title + " has been successfully downloaded as an audio file.")
    except Exception as e:
        print("An error occurred:", str(e))


video_url = input("Enter the YouTube video URL: ")
download_audio(video_url)
