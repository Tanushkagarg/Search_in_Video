'''
This is a function to filter transcripts obtained from YouTube videos.
This function takes a transcript (basically a json file which is the extracted text of that youtube video) as input and filters out entries with less than 5 words.
It utilizes the 're' module for pattern matching to extract words from the transcript entries.
The filtered transcript data is returned as a list of dictionaries.
'''

# Importing all the necessary modules

import re

def filter_yt_transcript(transcript):
    filtered_data = []
    for entry in transcript:
        # Extract the text from the entry
        text = entry["text"]

        # Use regular expression to find words in the text
        words = re.findall(r'\b\w+\b', text)
        if len(words) >= 5:
            filtered_data.append(entry)

    return filtered_data
