from pytube import YouTube 
import nltk
nltk.download('punkt', quiet=True)
import os 
from flask import *
from youtube_transcript_api import YouTubeTranscriptApi 
from tkinter import *
from tkinter import filedialog
import assemblyai as aai
from dotenv import load_dotenv
import spacy
from nltk import word_tokenize
import re
import json


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

app = Flask(__name__)

# Main Page to get the option
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form["option"]
        return redirect(url_for(('option'), select=option))
    return render_template('select.html')

# Route for handling the option
@app.route('/option', methods=['GET', 'POST'])
def option():
    select = request.args.get('select')
    
    if select == "youtube":
        if request.method == "POST":
            url = request.form["url"]
            # Extracting video ID from the URL
            id = url.split(".be/")[1]
            return redirect(url_for('youtube', id=id))
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
            return filedialog.askopenfilename(initialdir="C:\\Programming\\PythonFlask", title="Select a File", filetypes=(("MP3 Files", "*.mp3*"), ("Audio Files", "*.wav*"), ("all files", "*.*")))
        # Using tkinter 
        window = Tk()
        transcriber = aai.Transcriber()
        input_file = openFile()
        transcript = transcriber.transcribe(input_file)   
        result = transcript.export_subtitles_srt()
        window.destroy()
        
        # Converting the obtained srt file to a json file
        
        transcript = [dict(startTime = offset_seconds(startTime), endTime = offset_seconds(endTime), ref = ' '.join(ref.split())) for startTime, endTime, ref in re.findall(regex, result, re.DOTALL)]
        
        # Saving in Text Output folder and the name of .txt (transcripted file) will be the same as input file
        output_folder = "Text Output"
        
        # Create the output folder if it doesn't exist
        
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + ".json")
        
        # Remove stopwords from the transcript
        
        for chunk in transcript:
            chunk['ref'] = removeStopWords(chunk['ref'])
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(transcript, f)
        return transcript
                
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
    srt = YouTubeTranscriptApi.get_transcript(id)
    
    # Remove stopwords from the transcript
    
    for block in srt:
        block['text'] = removeStopWords(block['text'])
        
    
    #  Saving in Text Output folder and the name of .txt (transcripted file) will be the same as input file
    output_folder = "Text Output"
    output_file = os.path.join(output_folder, id + ".json")

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(srt, f)
    return srt

if __name__ == "__main__":
    app.run(debug=True)
