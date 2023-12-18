import pafy 
import os 
from pytube import YouTube 
import subprocess
from flask import *

app = Flask(__name__)

url = ""

# Main page to get the option
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form["option"]
        return redirect(url_for('download', option=option))
    else:
        return render_template('audioSelect.html')

# Route for handling the download process
@app.route('/download', methods=['GET', 'POST'])
def download():
    option = request.args.get('option')
    
    if request.method == 'POST':
        url = request.form["url"]
        
        # Download audio based on the selected option
        if option == "pytube":
            # Using pytube library
            yt = YouTube(url) 
            video = yt.streams.filter(only_audio=True).first() 

            destination = './output'

            out_file = video.download(output_path=destination) 

            base, ext = os.path.splitext(out_file) 
            new_file = base + '.mp3'
            os.rename(out_file, new_file) 

            print(yt.title + " has been successfully downloaded.")
            
            return render_template('downloading.html')
        
        elif option == "pafy":
            # Using pafy library
            video = pafy.new(url)
            audio_stream = video.getbestaudio()

            audio_stream.download()
            
            return render_template('downloading.html')
        
        elif option == "ytdl":
            # Using youtube-dl subprocess
            subprocess.run(["youtube-dl", "-f bestaudio", url])
            
            return render_template('downloading.html')
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
