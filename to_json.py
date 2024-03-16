'''
This script defines a function to convert segmented words with timestamps into JSON format.
The 'to_json' function takes segmented words, original filename, endpoint_sec, and length_limit as input parameters.
It defines a helper function 'second_to_timecode' to convert seconds to timecode format.
The '_helper' function is used internally to construct each entry in the JSON output.
The function iterates through the segmented words and creates sections based on endpoint_sec and length_limit.
For each section, it constructs a dictionary containing the text, start timestamp, and end timestamp.
The resulting list of dictionaries is written to a JSON file in the "JSON Output" folder with the format "{original_filename}_transcription.json".
The path to the generated JSON file is returned.
'''

# Importing necessary modules

import os
import json

def to_json(words, original_filename, endpoint_sec=1.0, length_limit=None):
    result = []

    def second_to_timecode(x):
        hour, x = divmod(x, 3600)
        minute, x = divmod(x, 60)
        second, x = divmod(x, 1)
        millisecond = int(x * 1000.)
        return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

    def _helper(start, end):
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

    file_name = os.path.splitext(os.path.basename(original_filename))[0]
    output_file_path = os.path.join("JSON Output", f"{file_name}_transcription.json")

    with open(output_file_path, 'w') as f:
        f.write(json.dumps(result, indent=2))

    return output_file_path
