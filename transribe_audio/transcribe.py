# dotenv: Used to load API key from a .env file 
# assemblyai: The library used for audio transcription
# pathlib: Provides convenient path manipulation tools
# tkinter: For displaying the file selection dialog

import os
from dotenv import load_dotenv
import assemblyai as aai
from pathlib import Path
from tkinter import filedialog, Tk


def load_api_key():
    """Loads the API key from a .env file."""
    load_dotenv()
    return os.getenv("API_KEY")


def select_audio_file():
    """Opens a file selection dialog and returns the chosen file path."""
    root = Tk()
    root.withdraw()
    filetypes = [("MP3 Files", "*.mp3"), ("Audio Files", "*.wav"), ("all files", "*.*")]
    title = "Select an Audio File"
    initialdir = Path.cwd() / "C:/Programming/PythonFlask"  # Adjust this based on your actual directory
    return filedialog.askopenfilename(initialdir=initialdir, title=title, filetypes=filetypes)


def transcribe_audio(file_path):
    """Transcribes an audio file and returns the text transcript."""
    aai.settings.api_key = load_api_key()
    transcriber = aai.Transcriber()
    result = transcriber.transcribe(file_path)
    return result.text


def main():
    """Runs the transcription process."""
    file_path = select_audio_file()
    if file_path:
        try:
            transcript = transcribe_audio(file_path)
            print(f"Transcript of '{Path(file_path).name}':")
            print(transcript)
        except Exception as e:
            print(f"Error transcribing file: {e}")
    else:
        print("No file selected or invalid file.")


if __name__ == "__main__":
    main()
