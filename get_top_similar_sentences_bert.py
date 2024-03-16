'''
This script defines a function to get the top similar sentences from a list of local/downloaded video transcript entries based on user input using BERT for similarity calculation.
Using the `calculate_similarity_bert` function, it calculates the cosine similarity between the user input and each sentence.
The function then pairs the similarity scores with sentences and timestamps, sorts them in descending order based on similarity scores, and returns the top 7 similar sentence pairs.
'''

# Importing all the necessary modules and functions
from operator import itemgetter
from calculate_similarity_bert import calculate_similarity_bert

def get_top_similar_sentences_bert(user_input, input_data):
    
    # Extracting sentences and timestamps from input data
    sentences = [entry["text"] for entry in input_data]
    timestamps = [entry["timestamp"] for entry in input_data]

    similarities = calculate_similarity_bert(user_input, sentences)

     # Pairing similarity scores with sentences and timestamps
    similarity_sentence_pairs = list(zip(similarities, sentences, timestamps))
    # Sorting pairs based on similarity scores in descending order
    similarity_sentence_pairs.sort(reverse=True, key=itemgetter(0))

    return similarity_sentence_pairs[:7]
