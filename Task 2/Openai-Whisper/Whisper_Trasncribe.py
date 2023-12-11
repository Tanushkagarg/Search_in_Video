# Transcribing the .wav (Audio file) using Openai-whisper Module

import os
import whisper

# User to enter the path of the input .wav file
input_file = input("Enter the path of the audio file: ")

# Check if the specified file exists
if not os.path.exists(input_file):
    print("Error: The specified file does not exist.")
    exit()

# Saving in Text Output folder and the name of .txt (transcripted file) will be the same as input file
output_folder = "Text Output"
output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + ".txt")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)


# Transcribes the .wav (audio input file) using Openai Whisper Module
model = whisper.load_model("base")
result = model.transcribe(input_file)

# Saving the result of transcription
with open(output_file, "w") as f:
    f.write(result["text"])

print(f"Transcription completed. Text saved to: {output_file}")