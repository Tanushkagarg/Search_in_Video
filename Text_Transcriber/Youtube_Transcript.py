from youtube_transcript_api import YouTubeTranscriptApi
import re

#Extract the video id form youtube audio
def get_youtube_video_id(youtube_link):
    pattern = r"(?<=v=)[\w-]+|(?<=be/)[\w-]+"
    match = re.search(pattern, youtube_link)
    if match:
        return match.group(0)
    else:
        return "Video ID not found or invalid link"
youtube_link = input("Enter the YouTube video link: ")
video_id = get_youtube_video_id(youtube_link)

# Get the transcript for the video
audio_transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Create a text file and store the transcript
with open(f"transcript.txt", "w", encoding="utf-8") as file:
        for line in audio_transcript:
            file.write(line['text'] + "\n")
