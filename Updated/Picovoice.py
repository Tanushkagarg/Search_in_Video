# Transcription using Leopard STT

import os
from typing import Sequence
import pvleopard
import json
from typing import Sequence, Union
from dotenv import load_dotenv



# Loading the API key of Leopard-STT API
load_dotenv()
leopard = pvleopard.create(access_key=os.getenv('KEY'))

# Take input file path from the user
input_file_path = input("Enter the path of the audio file: ")
transcript, words = leopard.process_file(input_file_path)


# Time Stamp Logic (HH:MM:SS,Millisecond)
def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)


# Transcribing the entire Audio File and storing it line by line 
def to_json(
        words: Sequence[pvleopard.Leopard.Word],
        endpoint_sec: float = 1.,
        length_limit: Union[None, int] = 64) -> str:
    result = []
    
    def _helper(start: int, end: int) -> dict:
        return {
            "text": ' '.join(x.word for x in words[start:(end + 1)]),
            "timestamp": {
                "start": second_to_timecode(words[start].start_sec),
                "end": second_to_timecode(words[end].end_sec)
            }
        }

    section_start = 0
    for k in range(1, len(words)):
        if ((words[k].start_sec - words[k - 1].end_sec) >= endpoint_sec) or \
                (length_limit is not None and (k - section_start) >= length_limit):
            result.append(_helper(section_start, k - 1))
            section_start = k

    result.append(_helper(section_start, len(words) - 1))

    # Get the filename from the input path
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = os.path.join("JSON Output", f"{file_name}.json")


# Writing the JSON file
    with open(output_file_path, 'w') as f:
        f.write(json.dumps(result, indent=2))

    return output_file_path

# Create the output folder if it doesn't exist
output_folder = "JSON Output"
os.makedirs(output_folder, exist_ok=True)

result_file_path = to_json(words)
print(f"Transcription saved to: {result_file_path}")





































































# from typing import Sequence
# import pvleopard
# import json
# from typing import Sequence, Union

# leopard = pvleopard.create(access_key="x6vS18pCLoz5HlGXq8vkND59LObOmBVEKr9Cgsy6FET9+8YdqXvnvg==")

# transcript, words = leopard.process_file("Audio Input\\2 Hours of English Conversation Practice - Improve Speaking Skills.wav")

# def second_to_timecode(x: float) -> str:
#     hour, x = divmod(x, 3600)
#     minute, x = divmod(x, 60)
#     second, x = divmod(x, 1)
#     millisecond = int(x * 1000.)

#     return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)


# def to_json(
#         words: Sequence[pvleopard.Leopard.Word],
#         endpoint_sec: float = 1.,
#         length_limit: Union[None, int] = 16) -> str:
#     result = []
    
#     def _helper(start: int, end: int) -> dict:
#         return {
#             "text": ' '.join(x.word for x in words[start:(end + 1)]),
#             "timestamp": {
#                 "start": second_to_timecode(words[start].start_sec),
#                 "end": second_to_timecode(words[end].end_sec)
#             }
#         }

#     section_start = 0
#     for k in range(1, len(words)):
#         if ((words[k].start_sec - words[k - 1].end_sec) >= endpoint_sec) or \
#                 (length_limit is not None and (k - section_start) >= length_limit):
#             result.append(_helper(section_start, k - 1))
#             section_start = k

#     result.append(_helper(section_start, len(words) - 1))

#     return json.dumps(result, indent=2)

# with open("trans4.json", 'w') as f:
#     f.write(to_json(words))

