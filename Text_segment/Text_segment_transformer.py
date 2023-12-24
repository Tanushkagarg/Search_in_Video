import spacy
import json



nlp = spacy.load("en_core_web_sm")

def filter_words(sentence):
    # Process the sentence using spaCy and exclude stop words
    doc = nlp(sentence)
    important_words = [token.text for token in doc if not token.is_stop]
    return ' '.join(important_words) if important_words else None

def create_output_folder():
    folder = Path("Output")
    folder.mkdir(exist_ok=True)
    return folder

def extract_data_from_json(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def process_data(data):
    output_data = []
    for entry in data:
        original_text = entry["text"]
        filtered_text = filter_words(original_text)

        if filtered_text is not None:
            output_data.append({
                "text": filtered_text,
                "timestamp": entry["timestamp"]
            })
    return output_data

def save_output(output_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(output_data, output_file, indent=2)
    print(f"output : {output_path}")

def transcribe(input_file_path):
    path_in = Path(input_file_path)
    folder = create_output_folder()
    input_filename = path_in.stem

    # Create output file name
    output_filename = f"Tagged - {input_filename}.json"
    output_path = folder / output_filename

    data = extract_data_from_json(path_in)
    processed_data = process_data(data)
    save_output(processed_data, output_path)

audio_transcript = input("Enter the file path : ")
transcribe(audio_transcript)
