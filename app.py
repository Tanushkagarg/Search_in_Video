from pytube import YouTube 
import os 
from flask import *
app = Flask(__name__)


url = ""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form["url"]
            
        yt = YouTube(url) 

        video = yt.streams.filter(only_audio=True).first() 

        print("Enter the destination (leave blank for current directory)") 
        destination = '.'

        out_file = video.download(output_path=destination) 

        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 

        print(yt.title + " has been successfully downloaded.")
        return render_template('downloading.html')
    
    else:
        return render_template('home.html')




if __name__ == "__main__":
    app.run()