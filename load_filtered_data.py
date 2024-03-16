'''
This script defines a function to load and filter data from a JSON file.
The 'load_filtered_data' function takes the path to a JSON file as input.
It loads the JSON data from the file and filters out entries with less than 5 words using regular expression.
The filtered data is returned as a list of dictionaries.
'''

# Importing necessary modules

import json
import re

def load_filtered_data(json_file_path):
    # Open the JSON file and load the data
    with open(json_file_path, 'r') as file:
        input_data = json.load(file)

    filtered_data = []
    for entry in input_data:
        # Extract the text from the entry
        text = entry["text"]
        words = re.findall(r'\b\w+\b', text)
        if len(words) >= 5:
            filtered_data.append(entry)

    return filtered_data
