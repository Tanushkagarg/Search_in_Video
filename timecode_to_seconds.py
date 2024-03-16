'''
This function converts time stamp of hh:mm:ss,milli seconds to seconds ignoring milli seconds so 
that it could be used in youtube url
'''

def timecode_to_seconds(timecode):
    parts = timecode.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2].split(',')[0])  # Ignore milliseconds
    return hours * 3600 + minutes * 60 + seconds
