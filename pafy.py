import pafy 
import os 
from flask import *

app = Flask(__name__)


url = ""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form["url"]
            
        video = pafy.new(url)

        audio_stream = video.getbestaudio()

        audio_stream.download()
        return render_template('downloading.html')
    
    else:
        return render_template('home.html')




if __name__ == "__main__":
    app.run()