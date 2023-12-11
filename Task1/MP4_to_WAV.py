import os
from pytube import YouTube

def extract_audio(url, output_path='Output in WAV'):
    try:
        # Fetching The video as an youtube object with the help of pytube module
        video = YouTube(url)

        # Storing the Audio stream of the video
        audio_stream = video.streams.filter(only_audio=True).first()

        # Downloading the audio on local storage
        audio_path = audio_stream.download(output_path=output_path)

        # Converting the downloaded audio to .wav and saving it in Output folder
        wav_path = os.path.splitext(audio_path)[0] + ".wav"
        os.rename(audio_path, wav_path)

        print(f"Audio extracted successfully: {wav_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    
    extract_audio(video_url)

## This module cannot access age restricted youtube videos