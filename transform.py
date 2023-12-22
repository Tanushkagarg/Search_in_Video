import spacy 
# Import Module 
import os 

# Folder Path 
path = "C:\\Programming\\Project\\Search_in_Video\\Text Output"

# Change the directory 
os.chdir(path) 

# Read text File 



# iterate through all file 

#load core english library 
nlp = spacy.load("en_core_web_sm") 
  
#take unicode string   
#here u stands for unicode 
# doc = nlp(u"I Love Coding. Geeks for Geeks helped me in this regard very much. I Love Geeks for Geeks.") 
str = "hello"
# print("{str}".format(str=str))

def read_text_file(file_path): 
    with open(file_path, 'r') as f: 
        str = (f.read()) 
    return str

#to print sentences 
for file in os.listdir(): 
    # Check whether file is in text format or not 
    if file.endswith(".txt"): 
        file_path = f"{path}\\{file}"
        # call read text file function 
        str = read_text_file(file_path) 

doc = nlp(u"{s}".format(s=str))

doc1 = list(doc.sents)
print(doc1[6])
doc2 = []
for chunk in doc1:
    sm = nlp(u"{s}".format(s=chunk))
    data = list(sm.sents)
    doc2.append(data)

# print(doc2)