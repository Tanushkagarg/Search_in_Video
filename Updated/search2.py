from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
import json
import re
from operator import itemgetter


model_name = 'sentence-transformers/paraphrase-miniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Function to calculate similarity between sentences using embeddings
def calculate_similarity_bert(user_input, sentences):
    # Tokenize user input
    input_tokens = tokenizer.encode_plus(user_input, max_length=128, truncation=True,
                                          padding='max_length', return_tensors='pt')

    # Tokenize sentences
    sentence_tokens = tokenizer(sentences, max_length=128, truncation=True, padding='max_length', return_tensors='pt')

    with torch.no_grad():
        input_embeddings = model(**input_tokens).last_hidden_state
        sentence_embeddings = model(**sentence_tokens).last_hidden_state


    input_mean_pooled = torch.mean(input_embeddings, dim=1)
    sentence_mean_pooled = torch.mean(sentence_embeddings, dim=1)


    input_mean_pooled = input_mean_pooled.detach().numpy()
    sentence_mean_pooled = sentence_mean_pooled.detach().numpy()


    similarities = cosine_similarity(input_mean_pooled, sentence_mean_pooled[0:])  # Exclude the user input
    return similarities.flatten()

# Function to get top similar sentences
def get_top_similar_sentences_bert(user_input, input_data):
    sentences = [entry["text"] for entry in input_data]
    timestamps = [entry["timestamp"] for entry in input_data]

    similarities = calculate_similarity_bert(user_input, sentences)

    # Pair similarities with sentences and timestamps
    similarity_sentence_pairs = list(zip(similarities, sentences, timestamps))
    similarity_sentence_pairs.sort(reverse=True, key=itemgetter(0))


    return similarity_sentence_pairs[:7]

def load_filtered_data(json_file_path):
    with open(json_file_path, "r") as file:
        input_data = json.load(file)

    filtered_data = []
    for entry in input_data:
        text = entry["text"]
        words = re.findall(r'\b\w+\b', text)
        if len(words) >= 5:
            filtered_data.append(entry)

    return filtered_data


json_file_path = input("Enter the path to the JSON file: ")

input_data = load_filtered_data(json_file_path)

user_input = input("Enter a sentence: ")

top_similar_sentences = get_top_similar_sentences_bert(user_input, input_data)

for similarity, text, timestamp in top_similar_sentences:
    print(f"\nSentence: {text}")
    print(f"Start Time: {timestamp['start']}")
    print(f"Similarity Score: {similarity:.4f}")
print("\n")
