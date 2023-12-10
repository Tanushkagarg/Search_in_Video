import os
from pytube import YouTube

def extract_audio(url, output_path='Output in WAV'):
    try:

        video = YouTube(url)

        audio_stream = video.streams.filter(only_audio=True).first()

        audio_path = audio_stream.download(output_path=output_path)

        wav_path = os.path.splitext(audio_path)[0] + ".wav"
        os.rename(audio_path, wav_path)

        print(f"Audio extracted successfully: {wav_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    
    extract_audio(video_url)
