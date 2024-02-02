# Updated version of the searching algorithm and JSON input formatted

**Pass the .wav or .mp3 file in ```Picovoice.py``` and get the JSON file containing transcription of the Audio**

**JSON file will be stored in ```JSON Output``` folder**

**Some pre-existing JSON files can be found in ```JSON Input``` folder**

**Pass the JSON file in which the search needs to implement in ```search2.py``` and pass the user query as well**

**Note:- User Query must be ```precise``` Avoid single, double or triple word queries and Pass only relative file paths**

**Getting Started with the project**



**Imports/Modules used**

1. ```pvleopard``` To transcribe the audio file
```
pip install pvleopard

```

2. ```dotenv``` To load the .env file used to protect API key being exploited
```
pip install python-dotenv
```

3. ```torch``` for embeddings
```
pip install torch
```

4. ```sentence-transformers``` for sementic search and tokenization and paraphrase model
```
pip install sentence-transformers
```

* Structure
  * .env file
    * Used to store the API key. For the API key [visit](https://console.picovoice.ai/)
  * Picovoice.py (STT code)
  * search2.py (Searching Algorithm)
  * Folder containing input audio files in .wav format
  * JSON Output folder wherin all the .json files will be saved
  * JSON Input folder containing demo input
