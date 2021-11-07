import mutagen
from mutagen.wave import WAVE

# function to convert the information into 
# some readable format
# def audio_duration(length):
#     hours = length // 3600  # calculate in hours
#     length %= 3600
#     mins = length // 60  # calculate in minutes
#     length %= 60
#     seconds = length  # calculate in seconds

#     return hours, mins, seconds  # returns the duration


def get_time(file):
    
    # Create a WAVE object
    # Specify the directory address of your wavpack file
    # "alarm.wav" is the name of the audiofile
    audio = WAVE(file)
    
    # contains all the metadata about the wavpack file
    audio_info = audio.info
    length = int(audio_info.length)
    return length