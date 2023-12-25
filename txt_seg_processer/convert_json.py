# convert txt file to json file
import tkinter as tk
from tkinter import filedialog
import json
import os 
def select_file():
    """Opens a file selection dialog and returns the chosen file path."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select TXT File",
        filetypes=(("Text Files", "*.txt"),)
    )
    root.destroy()  # Close the Tkinter instance
    return file_path

def convert_txt_to_json(input_file_path):
    """Converts a TXT file to JSON and saves the output."""

    with open(input_file_path, 'r', encoding='utf-8') as file:
        txt_data = file.read()

    output_filename = os.path.splitext(os.path.basename(input_file_path))[0] + ".json"
    output_path = os.path.join("Output", output_filename)  # Save to "Output" folder

    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(txt_data, output_file, indent=2)

    print(f"TXT to JSON conversion completed. Output saved to: {output_path}")

# Get input file path using Tkinter
input_file_path = select_file()
if input_file_path:
    convert_txt_to_json(input_file_path)
else:
    print("No file selected.")
