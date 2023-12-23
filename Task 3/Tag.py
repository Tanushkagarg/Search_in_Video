import os
import spacy
import json

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def filter_important_words(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)

    # Exclude stop words
    important_words = [token.text for token in doc if not token.is_stop]

    # Return the altered sentence or None if no important words
    return ' '.join(important_words) if important_words else None

# Creating an Output folder (it it doenst Exist)
def process_transcript(input_file_path):
    output_folder = "Output"
    os.makedirs(output_folder, exist_ok=True)

    # Extract input file name without extension
    input_filename, _ = os.path.splitext(os.path.basename(input_file_path))

    # Create output file name
    output_filename = f"Tagged - {input_filename}.json"
    output_path = os.path.join(output_folder, output_filename)

# Reading the Input .json file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    output_data = []

    for entry in data:
        original_text = entry["text"]
        filtered_text = filter_important_words(original_text)

        if filtered_text is not None:
            output_data.append({
                "text": filtered_text,
                "timestamp": entry["timestamp"]
            })

# After reading removing the stop words and then saves the new .json file (As "Tagged - {Input_File_Name}.json") in Output Folder

    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, indent=2)

    print(f"Processing completed. Output saved to: {output_path}")

# Takes in the path of the Input file
input_file_path = input("Enter the path of the JSON file: ")
process_transcript(input_file_path)
