import aubio
import numpy as np
import pyaudio
import sys
from mutagen.mp3 import MP3
import get_time


# Some constants for setting the PyAudio and the
# Aubio.
BUFFER_SIZE             = 2048
CHANNELS                = 1
FORMAT                  = pyaudio.paFloat32
METHOD                  = "default"
SAMPLE_RATE             = 1000
HOP_SIZE                = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME    = HOP_SIZE

def main(args):

    # Initiating PyAudio object.
    pA = pyaudio.PyAudio()
    # Open the microphone stream.
    mic = pA.open(format=FORMAT, channels=CHANNELS,
        rate=SAMPLE_RATE, input=True,
        frames_per_buffer=PERIOD_SIZE_IN_FRAME)

    # Initiating Aubio's pitch detection object.
    pDetection = aubio.pitch(METHOD, BUFFER_SIZE,
        HOP_SIZE, SAMPLE_RATE)
    # Set unit.
    pDetection.set_unit("Hz")
    # Frequency under -40 dB will considered
    # as a silence.
    pDetection.set_silence(-40)

    # Getting a list of pitches and volumes
    pitches = []
    volumes = []

    # Import the time of the music file
    time = get_time.get_time("/Users/ongtjunjet/Downloads/Geometry Dash - Stereo Madness [FULL SONG DOWNLOAD].wav")

    # Infinite loop!
    while time > 0:
        # Always listening to the microphone.
        data = mic.read(PERIOD_SIZE_IN_FRAME)
        # Convert into number that Aubio understand.
        samples = np.fromstring(data,
            dtype=aubio.float_type)
        # Finally get the pitch.
        pitch = pDetection(samples)[0]
        # Compute the energy (volume)
        # of the current frame.
        volume = np.sum(samples**2)/len(samples)
        # Format the volume output so it only
        # displays at most six numbers behind 0.
        volume = "{:6f}".format(volume)

        # Finally print the pitch and the volume.
        pitches.append(str(pitch))
        volumes.append(str(volume))
        print(str(pitch) + " " + str(volume))
        time -= 1
    
    print(pitches)
    print(volumes)

if __name__ == "__main__": main(sys.argv)