from flask import *
import subprocess

app = Flask(__name__)


url = ""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form["url"]
            
        subprocess.run(["youtube-dl", "-f bestaudio", url])

        return render_template('downloading.html')
    
    else:
        return render_template('home.html')




if __name__ == "__main__":
    app.run()