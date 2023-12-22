import re
import json

regex = r'(?:\d+)\s(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)\s+(.+?)(?:\n\n|$)'
offset_seconds = lambda ts: sum(howmany * sec for howmany, sec in zip(map(int, ts.replace(',', ':').split(':')), [60 * 60, 60, 1, 1e-3]))

transcript = [dict(startTime = offset_seconds(startTime), endTime = offset_seconds(endTime), ref = ' '.join(ref.split())) for startTime, endTime, ref in re.findall(regex, open('C:\\Programming\\Project\\Search_in_Video\\Text Output\\Python GUI open a file (filedialog) 📁.srt').read(), re.DOTALL)]

print(type(transcript))
with open('data.json','w', encoding='utf-8') as f:
    json.dump(transcript ,f)
