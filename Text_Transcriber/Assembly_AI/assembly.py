import os
import requests
import time
import json

API_KEY = "API_KEY"
audio_file_path = "extracted_audio.wav"  # Replace with the path to audio file

def upload_audio_file(api_key, audio_path):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    headers = {
        "authorization": api_key,
    }

    with open(audio_path, "rb") as file:
        audio_data = file.read()

    response = requests.post(endpoint, headers=headers, files={"audio": audio_data})

    return response.json()["id"]

def get_transcript(api_key, transcript_id):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }

    while True:
        response = requests.get(endpoint, headers=headers)
        data = response.json()

        if data["status"] == "completed":
            return data["text"]
        elif data["status"] == "failed":
            raise Exception("Transcription failed")
        
        time.sleep(5)

def save_transcript_to_file(transcript_text, output_file_path):
    with open(output_file_path, "w") as file:
        file.write(transcript_text)

# Upload audio file for transcription
transcript_id = upload_audio_file(API_KEY, audio_file_path)

# get the transcript
transcript = get_transcript(API_KEY, transcript_id)

# Save it it as text file
output_text_file_path = "transcript.txt"
save_transcript_to_file(transcript, output_text_file_path)

print(f"Transcript saved to {output_text_file_path}")
