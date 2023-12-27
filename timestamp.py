from flask import *
from tkinter import *
from tkinter import filedialog
import os

app = Flask(__name__, static_folder='Audio Output')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        time = request.form["time"]
        def openFile():
            return filedialog.askopenfilename(initialdir=".", title="Select a File", filetypes=(("MP3 Files", "*.mp3*"), ("Audio Files", "*.wav*"), ("all files", "*.*")))
        # Using tkinter
        window = Tk()
        filePath = openFile()
        window.destroy()
        print(filePath)
        static_folder = os.path.join(os.getcwd(), 'Audio Output')

        relative_path = os.path.relpath(filePath.replace('\\', '/'), start=static_folder)

        return render_template('audio.html', time=time, filePath=relative_path)    
    return render_template('timestamp.html')

if __name__ == '__main__':
    app.run(debug=True)