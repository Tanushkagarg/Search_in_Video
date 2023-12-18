from youtube_transcript_api import YouTubeTranscriptApi


def transcribe_youtube(video_id):
    """Transcribes audio from a YouTube video using its ID."""
    srt = YouTubeTranscriptApi.get_transcript(video_id)
    return srt


def main():
    """Prompts user for YouTube video ID, transcribes it, and prints the transcript."""
    video_id = input("Enter the YouTube video ID: ")
    transcript = transcribe_youtube(video_id)
    print(f"\nTranscript:\n{transcript}")


if __name__ == "__main__":
    main()
