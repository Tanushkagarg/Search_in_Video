'''
This Flask application provides a platform for users to upload and search for specific segments of videos. It supports local video files and YouTube videos for now and will support Coursera videos in future. The application utilizes various libraries and APIs for processing audio, extracting transcripts, and calculating semantic similarity between sentences. Users can upload files, search for specific sentences, and play corresponding video segments. Additionally, the application supports searching within YouTube videos by extracting their transcripts or audio if available.
'''

# Importing all the necessary modules and functions

from typing import Sequence, Union
from flask import Flask, render_template, request, send_file, redirect, send_from_directory, url_for
import os
from pydub import AudioSegment
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import VideoFileClip
import spacy
import io
import json
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch
import re
from operator import itemgetter
import pvleopard
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
from to_json import to_json
from timecode_to_seconds import timecode_to_seconds
from calculate_similarity_bert import calculate_similarity_bert
from get_top_similar_sentences_bert import get_top_similar_sentences_bert
from get_top_similar_sentences_bert_yt import get_top_similar_sentences_bert_yt
from load_filtered_data import load_filtered_data
from filter_yt_transcript import filter_yt_transcript

# Initializing Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Loading Models
nlp = spacy.load('en_core_web_lg')
load_dotenv()
leopard = pvleopard.create(access_key=os.getenv('KEY'))
model_name = 'sentence-transformers/paraphrase-miniLM-L6-v2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Global variable to store the uploaded filename
uploaded_filename = None

# Creating the 'uploads' folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

# Folder for storing JSON output
json_output_folder = "JSON Output"
if not os.path.exists(json_output_folder):
    os.makedirs(json_output_folder)

# Upload Route
@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_filename

    # Checking if the file is included in the request
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # If a file is uploaded
    if file:
        uploaded_filename = file.filename

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            json_filename = f"{os.path.splitext(file.filename)[0]}_transcription.json"
            json_file_path = os.path.join(json_output_folder, json_filename)

             # Checking if transcription already exists for faster performance
            if os.path.exists(json_file_path):
                return file.filename

            # Extracting audio from the video and even extracting its STT using PVleopard
            video_clip = VideoFileClip(file_path)
            audio_folder = "Audio Output"
            os.makedirs(audio_folder, exist_ok=True)
            audio_file_path = os.path.join(audio_folder, f"{file.filename}_audio.wav")
            video_clip.audio.write_audiofile(audio_file_path, codec='pcm_s16le', fps=44100)
            transcript, words = leopard.process_file(audio_file_path)
            to_json(words, file.filename)

            return file.filename

# Route to deal with local Files
@app.route('/local_storage', methods=['GET', 'POST'])
def local_storage():
    global uploaded_filename

    if request.method == 'POST':
        sentence = request.form.get('search-sentence')

        # Getting the STT json file of the perticular video uploaded
        json_filename = f"{os.path.splitext(uploaded_filename)[0]}_transcription.json"
        json_file_path = os.path.join(json_output_folder, json_filename)

        if os.path.exists(json_file_path):
                transcript = load_filtered_data(json_file_path)
        else:
            return render_template('local_storage.html', error="Transcript not found for the selected file.")

        # Sending the filtered json STT to get the most similar sentences
        top_similar_sentences = get_top_similar_sentences_bert(sentence, transcript)
        sentences = [entry[1] for entry in top_similar_sentences]   # Similar Sentences
        start_time = [entry[2]['start'] for entry in top_similar_sentences]   # Their corresponding start time

        return redirect(url_for('play_searched_local_video', video_filename=uploaded_filename, start_time=start_time))

    return render_template('local_storage.html')

# Route for playing searched local video
@app.route('/play/<filename>')
def play(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))
    return send_file(file_path, as_attachment=True)

# Route for playing searched local video with initial start time as 00:00:00
@app.route('/play_searched_local_video')
def play_searched_local_video():
    video_filename = request.args.get('video_filename')
    start_time_str = request.args.get('start_time', '00:00:00,000') 
    h, m, s_ms = start_time_str.split(':')
    s, ms = s_ms.split(',')

    start_time = int(h) * 3600 + int(m) * 60 + int(s)  / 1000.0
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)

    return render_template('play_searched_local_video.html', video_filename=video_filename, start_time=start_time)

# Function to clean the youtube title
def clean_filename(title):
    invalid_chars = '\/:*?"<>|'
    cleaned_title = ''.join(char for char in title if char not in invalid_chars)
    return cleaned_title

# New Route to deal with youtube videos
@app.route('/youtube', methods=['GET', 'POST'])
def youtube():
    if request.method == 'POST':
        video_url = request.form.get('youtube-link')

        # Get the youtube video and its information from the link
        video_id = video_url.split("v=")[1].split("&")[0]
        yt = YouTube(video_url)
        video_title = yt.title

        cleaned_title = clean_filename(video_title)
        return render_template('youtube.html', video_title=video_title,  video_id = video_id)

    return render_template('youtube.html')

# Route to deal with seaching in youtube videos
@app.route('/search_sentence', methods=['POST'])
def search_sentence():
    if request.method == 'POST':
        video_id = request.form.get('video_id')
        sentence = request.form.get('search-sentence')

        # Fetching the transcript of that perticular video from Youtube Transcript API
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])

            # If the transcript exits in english then procceed to filter it
            if transcript:
                input_data = filter_yt_transcript(transcript)

            top_similar_sentences = get_top_similar_sentences_bert_yt(sentence, input_data)
            sentences = [entry[1] for entry in top_similar_sentences]
            start_times = [int(float(entry[2])) for entry in top_similar_sentences]

            return render_template('video_player.html', video_id=video_id, start_times=start_times, sentences=sentences)

# If the transcript of that video are disabled or not found then extract its audio in .wav format
        # and extract its text using PVleopard and store it as json file
        except (NoTranscriptFound, TranscriptsDisabled):
            json_file_path = os.path.join(json_output_folder, f"{video_id}_transcription.json")
            
            # Check if the json file exists or not for faster results
            if os.path.exists(json_file_path):
                input_data = load_filtered_data(f"JSON Output/{video_id}_transcription.json")

            else:
                audio_file_path = f"Audio Output/{video_id}.wav"
                yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
                yt.streams.filter(only_audio=True).first().download(output_path="Audio Output", filename=video_id+".wav")
                transcript, words = leopard.process_file(audio_file_path)

                to_json(words, f"{video_id}.wav")
                input_data = load_filtered_data(f"JSON Output/{video_id}_transcription.json")

            top_similar_sentences = get_top_similar_sentences_bert(sentence, input_data)

            sentences = [entry[1] for entry in top_similar_sentences]
            start_times =[entry[2]['start'] for entry in top_similar_sentences]
            start_times_seconds = [timecode_to_seconds(timecode) for timecode in start_times]

            return render_template('video_player.html', video_id=video_id, start_times=start_times_seconds)

    return render_template('video_player.html')

# New Route to deal with coursera videos [Will be added in future]
@app.route('/coursera', methods=['GET', 'POST'])
def coursera():
    if request.method == 'POST':
        pass
    return render_template('coursera.html')

# Dropdown select functionality in index.html
@app.route('/select', methods=['POST'])
def select():
    selected_option = request.form.get('media-platform')

    if selected_option == 'local_storage':
        return redirect('/local_storage')
    elif selected_option == 'youtube':
        return redirect('/youtube')
    elif selected_option == 'coursera':
        return redirect('/coursera')
    else:
        return redirect('/')

# Running the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)