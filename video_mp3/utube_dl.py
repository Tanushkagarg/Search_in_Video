import youtube_dl

def download_audio(link):
    output_path = 'audio_file.mp3'  #Replace this with your desired output path and file name

    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': output_path,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([link])

if __name__ == "__main__":
    video_link = input("Enter the video link: ")
    download_audio(video_link)
