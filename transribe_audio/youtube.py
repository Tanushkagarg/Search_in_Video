from youtube_transcript_api import YouTubeTranscriptApi

def transcribe_youtube(video_id):
    """Transcribes audio from a YouTube video using its ID."""
    srt = YouTubeTranscriptApi.get_transcript(video_id)
    return srt

def format_transcript_with_timestamps(transcript):
    """Formats transcript content with timestamps."""
    formatted_transcript = ""
    for line in transcript:
        formatted_transcript += f"[{line['start']} - {line['duration']}] {line['text']}\n"
    return formatted_transcript

def save_transcript_to_file(transcript, file_name):
    """Saves the transcript content into a text file."""
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(transcript)

def main():
    """Prompts user for YouTube video ID, transcribes it, and saves the transcript in a file."""
    video_id = input("Enter the YouTube video ID: ")
    transcript = transcribe_youtube(video_id)
    
    formatted_transcript = format_transcript_with_timestamps(transcript)
    
    file_name = f"{video_id}_transcript.txt"  # File name based on video ID
    save_transcript_to_file(formatted_transcript, file_name)
    print(f"\nTranscript saved to '{file_name}'.")

if __name__ == "__main__":
    main()
