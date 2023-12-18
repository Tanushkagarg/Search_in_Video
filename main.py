from pytube import YouTube 
import os 
from flask import *
from youtube_transcript_api import YouTubeTranscriptApi 
from tkinter import *
from tkinter import filedialog
import assemblyai as aai
from dotenv import load_dotenv
import pvleopard


load_dotenv()

aai.settings.api_key = os.getenv('API_KEY')

# leopard = pvleopard.create(access_key=os.getenv('PICO_KEY'))

def transcribe_audio(file_path):
    output_folder = "Text Output"
    output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(file_path))[0] + ".txt")
    os.makedirs(output_folder, exist_ok=True)
    transcriber = aai.Transcriber()
    result = transcriber.transcribe(file_path)

    with open(output_file, "w") as f:
        f.write(result.text)
    return result.text

# def transcribe_audio_pico(audio_path):
#     transcript, words = leopard.process_file(audio_path)
#     return transcript

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form["option"]
        return redirect(url_for(('option'), select=option))
    return render_template('select.html')


@app.route('/option', methods=['GET', 'POST'])
def option():
    select = request.args.get('select')
    if select == "youtube":
        if request.method == "POST":
            url = request.form["url"]
            id = url.split(".be/")[1]
            return redirect(url_for('youtube', id=id))
        return render_template("youtube.html")
    elif select == "udemy":
        if request.method == "POST":
            access_token = request.form["access_token"]
            return redirect(url_for('udemy', access_token=access_token))
        return render_template("access.html")
    elif select == "local":
        def openFile():
            filepath = filedialog.askopenfilename(initialdir="C:\\Programming\\PythonFlask", title="Select a File", filetypes=(("MP3 Files", "*.mp3*"), ("Audio Files", "*.wav*"), ("all files", "*.*")))
            return filepath
        window = Tk()
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(openFile())   
        result = transcript.export_subtitles_vtt()
        # resultPico = transcribe_audio_pico(openFile())
        window.destroy()
        return result
                
    return "hello"

@app.route('/udemy/', methods=['GET', 'POST'])
def srt(access_token):
    if request.method == "POST":
        url = request.form["url"]
        return redirect(url_for('udemy', url=url))

@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    id = request.args.get('id')
    srt = YouTubeTranscriptApi.get_transcript(id)
    return srt


if __name__ == "__main__":
    app.run(debug=True)