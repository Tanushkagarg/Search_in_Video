import tkinter as tk
from tkinter import filedialog
import os
import spacy
import json

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def filter_important_words(sentence):
    """Filters out stop words from a sentence and returns a string of important words."""
    doc = nlp(sentence)
    important_words = [token.text for token in doc if not token.is_stop]
    return ' '.join(important_words) if important_words else None

def process_transcript(input_file_path):
    """Processes a JSON transcript to remove stop words and saves a tagged version."""

    # Create output folder if it doesn't exist
    output_folder = "Output"
    os.makedirs(output_folder, exist_ok=True)

    # Generate output file name
    input_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    output_filename = f"Tagged - {input_filename}.json"
    output_path = os.path.join(output_folder, output_filename)

    # Load input data
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON file: {e}")
        return

    # Process transcript entries
    output_data = []
    for entry in data:
        if isinstance(entry["text"], list):  # Handle list of strings
            for text_item in entry["text"]:
                filtered_text = filter_important_words(text_item)
                if filtered_text:
                    output_data.append({"text": filtered_text, "timestamp": entry["timestamp"]})
        else:  # Handle string value
            filtered_text = filter_important_words(entry["text"])
            if filtered_text:
                output_data.append({"text": filtered_text, "timestamp": entry["timestamp"]})

    # Save processed data to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            json.dump(output_data, output_file, indent=2)
        print(f"Processing completed. Output saved to: {output_path}")
    except OSError as e:
        print(f"Error saving output file: {e}")

def select_file():
    """Opens a file selection dialog and returns the chosen file path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select JSON Transcript",
        filetypes=(("JSON Files", "*.json"),)
    )
    root.destroy()  # Close the Tkinter instance
    return file_path

# Get input file path using Tkinter
input_file_path = select_file()
if input_file_path:
    process_transcript(input_file_path)
else:
    print("No file selected.")
