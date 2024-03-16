'''
This script imports necessary modules and functions for calculating cosine similarity using a pre-trained BERT model.
It loads the BERT model and tokenizer from the Hugging Face transformers library.
The calculate_similarity_bert function calculates the cosine similarity between a user input sentence and a list of sentences.
'''

# Importing all the necessary modules and functions

import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel

# Loading the Model and tokenizing
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-miniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/paraphrase-miniLM-L6-v2')

# Function to calculate the cosine similarity provided by sklearn
def calculate_similarity_bert(user_input, sentences):
    # Tokenizing user input and sentences
    input_tokens = tokenizer.encode_plus(user_input, max_length=128, truncation=True,
                                          padding='max_length', return_tensors='pt')

    sentence_tokens = tokenizer(sentences, max_length=128, truncation=True, padding='max_length', return_tensors='pt')

    # Extracting embeddings for user input and sentences using BERT model
    with torch.no_grad():
        input_embeddings = model(**input_tokens).last_hidden_state
        sentence_embeddings = model(**sentence_tokens).last_hidden_state

    # Calculating mean-pooled embeddings
    input_mean_pooled = torch.mean(input_embeddings, dim=1)
    sentence_mean_pooled = torch.mean(sentence_embeddings, dim=1)

    # Converting embeddings to numpy arrays
    input_mean_pooled = input_mean_pooled.detach().numpy()
    sentence_mean_pooled = sentence_mean_pooled.detach().numpy()

    similarities = cosine_similarity(input_mean_pooled, sentence_mean_pooled[0:])
    return similarities.flatten()
