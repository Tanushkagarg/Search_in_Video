import spacy
import json
from operator import itemgetter

# Load Spacy English model
nlp = spacy.load("en_core_web_md")

# Function to calculate similarity between sentences
def calculate_similarity(input_text, reference_text):
    input_doc = nlp(input_text)
    reference_doc = nlp(reference_text)
    return input_doc.similarity(reference_doc)

# Function to get top 7 similar sentences
def get_top_similar_sentences(user_input, input_data):
    similarities = []

# Calculating the similarity of the user entered statement and appending it to similarities list
    for entry in input_data:
        similarity_score = calculate_similarity(user_input, entry["text"])
        similarities.append({"entry": entry, "similarity": similarity_score})

    # Sort by similarity score in descending order
    similarities.sort(key=itemgetter("similarity"), reverse=True)

    # Return top 7 similar sentences with timestamps and similarity scores
    top_similar_sentences = similarities[:7]
    return [(entry["entry"]["text"], entry["entry"]["timestamp"], entry["similarity"]) for entry in top_similar_sentences]

# Get the path to the JSON file from the user
json_file_path = input("Enter the path to the JSON file: ")

# Load input data from JSON file
with open(json_file_path, "r") as file:
    input_data = json.load(file)

# Taking the sentence from the user
user_input = input("Enter a sentence: ")
# Passing the file data as input_data and the sentence entered as user_data for calculating similarities
top_similar_sentences = get_top_similar_sentences(user_input, input_data)

# Printing the top 7 similar sentences with its text, timestamp and its similarity
for text, timestamp, similarity in top_similar_sentences:
    print(f"\nSentence: {text}")
    print(f"Timestamp: {timestamp['start']} to {timestamp['end']}")
    print(f"Similarity Score: {similarity:.4f}")
print("\n")
