from flask import Flask, render_template, request, send_file
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Creating Uploads folder if not present
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Redering index.html to fetch data
@app.route('/')
def index():
    return render_template('index.html')

'''
User choosen file from thier local system will be saved in uploads
checking if that file exist if exist then upload it via POST method
'''
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return file.filename
    
# Playing the selected file
@app.route('/play/<filename>')
def play(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if filename.lower().endswith(('.mp3', '.wav')):
        # Converting the audio file to WAV for compatibility
        audio = AudioSegment.from_file(file_path)
        wav_path = os.path.splitext(file_path)[0] + '.wav'
        audio.export(wav_path, format='wav')
        return send_file(wav_path, as_attachment=True)

    elif filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
        # No need to convert video files
        return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
