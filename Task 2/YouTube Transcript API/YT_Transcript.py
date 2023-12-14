
# Transcribe Youtube Video using Youtube Transcript API

import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to clean the title for using it as a filename
def clean_filename(title):
    # Remove invalid characters from the title
    invalid_chars = '\/:*?"<>|'
    cleaned_title = ''.join(char for char in title if char not in invalid_chars)
    return cleaned_title

# Input: YouTube video URL
video_url = input("Enter the YouTube video URL: ")

# Get video ID from the URL
video_id = video_url.split("v=")[1].split("&")[0]

# Get video information using pytube
yt = YouTube(video_url)
video_title = yt.title

# Clean the title for using it as a filename
cleaned_title = clean_filename(video_title)

# Create the 'Subtitles' directory if it doesn't exist
create_directory("Subtitles")

# Get the transcript for the video
transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

# Define the filename for the subtitles file
filename = f"Subtitles/{cleaned_title}.txt"

# Write the transcript to the subtitles file
with open(filename, "w") as f:
    for entry in transcript:
        f.write("{}\n".format(entry))

print(f"Subtitles saved to: {filename}")
