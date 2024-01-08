from pytube import YouTube 
import nltk
import os 
from flask import *
from youtube_transcript_api import YouTubeTranscriptApi 
from tkinter import *
from tkinter import filedialog
import assemblyai as aai
from dotenv import load_dotenv
import spacy
import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk_data_path = "."  # Set your desired directory path

# Check if the punkt package is already downloaded, if not, download it
if not os.path.exists(os.path.join(nltk_data_path, 'tokenizers', 'punkt')):
    nltk.download('punkt', download_dir=nltk_data_path)

# Set the nltk data path to the specified directory
nltk.data.path.append(nltk_data_path)

from nltk import word_tokenize

regex = r'(?:\d+)\s(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\s+(.+?)(?:\n\n|$)'
offset_seconds = lambda ts: sum(howmany * sec for howmany, sec in zip(map(int, ts.replace(',', ':').split(':')), [60 * 60, 60, 1, 1e-3]))

# Load environment variables from a .env file
load_dotenv()

#using spacy and nltk

sp = spacy.load("en_core_web_sm") 

all_stopwords = sp.Defaults.stop_words

aai.settings.api_key = os.getenv('API_KEY')

# Function to transcribe audio using AssemblyAI
def transcribe_audio(file_path):
    output_folder = "Text Output"
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + ".srt")
   
    # Create the output folder if it doesn't exist
   
    os.makedirs(output_folder, exist_ok=True)
    transcriber = aai.Transcriber()
    result = transcriber.transcribe(file_path)

    # Write the transcription result to a text file
    with open(output_file, "w") as f:
        f.write(result.text)
    return result.text

# function to remove stopwords for a particular chunk of text 

def removeStopWords(text):
    text_tokens = word_tokenize(text)
    tokens_without_sw= [word for word in text_tokens if not word in all_stopwords]
    return tokens_without_sw

app = Flask(__name__, static_folder='Audio Output')

# Main Page to get the option
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form["option"]
        inputText = request.form["inputText"] 
        return redirect(url_for(('option'), select=option, inputText=inputText))
    return render_template('select.html')

# Route for handling the option
@app.route('/option', methods=['GET', 'POST'])
def option():
    select = request.args.get('select')
    inputText = request.args.get('inputText')
    if select == "youtube":
        if request.method == "POST":
            url = request.form["url"]
            # Extracting video ID from the URL
            id = url.split(".be/")[1]
            return redirect(url_for('youtube', id=id, input=inputText))
        return render_template("youtube.html")
    
    # Handle Udemy option
    elif select == "udemy":
        if request.method == "POST":
            access_token = request.form["access_token"]
            return redirect(url_for('udemy', access_token=access_token))
        return "<h1>Still working on it<h1>"
    
    # Handle local file option
    elif select == "local":
        

        
        def openFile():
            return filedialog.askopenfilename(initialdir=".", title="Select a File", filetypes=(("MP3 Files", "*.mp3*"), ("Audio Files", "*.wav*"), ("all files", "*.*")))
        # Using tkinter 
        window = Tk()
        transcriber = aai.Transcriber()
        input_file = openFile()
        transcript = transcriber.transcribe(input_file)   
        result = transcript.export_subtitles_srt()
        window.destroy()
        static_folder = os.path.join(os.getcwd(), 'Audio Output')

        relative_path = os.path.relpath(input_file.replace('\\', '/'), start=static_folder)
        # Converting the obtained srt file to a json file
        
        transcript = [dict(startTime = offset_seconds(startTime), endTime = offset_seconds(endTime), ref = ' '.join(ref.split())) for startTime, endTime, ref in re.findall(regex, result, re.DOTALL)]
        
        # Saving in Text Output folder and the name of .txt (transcripted file) will be the same as input file
        output_folder = "Text Output"
        
        # Create the output folder if it doesn't exist
        title = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_folder, title + ".json")
        
        # Remove stopwords from the transcript
        
        for chunk in transcript:
            chunk['ref'] = removeStopWords(chunk['ref'])
            
        inputText = removeStopWords(inputText)
        
        processed_srt_data = [' '.join(entry['ref']) for entry in transcript]
        processed_input = ' '.join(inputText)
    
    
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(processed_srt_data + [processed_input])

        cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        most_similar_index = cosine_similarities.argmax()
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(transcript, f)
        return render_template('audio.html', time=transcript[most_similar_index]["startTime"], filePath=relative_path)    
                
    # Default response if the option is not recognized
    return "<h1>Still working on it<h1>"

# Route for handling Udemy option
@app.route('/udemy/', methods=['GET', 'POST'])
def srt(access_token):
    if request.method == "POST":
        url = request.form["url"]
        return redirect(url_for('udemy', url=url))

# Route for handling YouTube option
@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    id = request.args.get('id')
    input = request.args.get('input')
    srt = YouTubeTranscriptApi.get_transcript(id)
    
    input = removeStopWords(input)
    
    # Remove stopwords from the transcript
    
    for block in srt:
        block['text'] = removeStopWords(block['text'])
    processed_srt_data = [' '.join(entry['text']) for entry in srt]
    processed_input = ' '.join(input)
    
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_srt_data + [processed_input])

    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    most_similar_index = cosine_similarities.argmax()

    #  Saving in Text Output folder and the name of .txt (transcripted file) will be the same as input file
    output_folder = "Text Output"
    output_file = os.path.join(output_folder, id + ".json")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(srt, f)
    return (srt[most_similar_index])

@app.route('/input', methods=['GET', 'POST'])
def input():
    id = request.args.get('id')    
    if request.method == "POST":
        file_path = 'Text Output/' + id + '.json'
        
        with open(file_path, 'r') as file:
            content = file.read()
        print(content)
        
        text = request.form["input"]
        
    return render_template("input.html")

if __name__ == "__main__":
    app.run(debug=True)
