from pytube import YouTube 
import os 
from flask import *
from youtube_transcript_api import YouTubeTranscriptApi 
from tkinter import *
from tkinter import filedialog
import assemblyai as aai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

aai.settings.api_key = os.getenv('API_KEY')

# Function to transcribe audio using AssemblyAI
def transcribe_audio(file_path):
    output_folder = "Text Output"
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + ".txt")
   
    # Create the output folder if it doesn't exist
   
    os.makedirs(output_folder, exist_ok=True)
    transcriber = aai.Transcriber()
    result = transcriber.transcribe(file_path)

    # Write the transcription result to a text file
    with open(output_file, "w") as f:
        f.write(result.text)
    return result.text

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
        # Saving in Text Output folder and the name of .txt (transcripted file) will be the same as input file
        output_folder = "Text Output"
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(input_file))[0] + ".txt")

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        with open(output_file, "w") as f:
            f.write(result)
        return result
                
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
