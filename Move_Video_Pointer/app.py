from flask import Flask, render_template, request, send_from_directory
from moviepy.editor import *
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def move_video_pointer(video_file, timestamp):
    video = VideoFileClip(video_file)
    video = video.subclip(timestamp)
    video.write_videofile('output.mp4')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        timestamp = request.form.get('timestamp')
        video_file = request.files['video_file']
        video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename))
        move_video_pointer(os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename), timestamp)
        return render_template('index.html', message=f'Video pointer moved to {timestamp} seconds')
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
