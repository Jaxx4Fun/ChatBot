import pyaudio
from pyaudio import paInt16
import wave
RATE = 16000
FORMAT = paInt16
CHANNELS = 1
FRAMES_PER_BUFFER = 1024
pa = pyaudio.PyAudio()
stream = pa.open(rate=RATE,
                format=FORMAT,
                channels=CHANNELS,
                input=True)
while True:
    data = stream.read(FRAMES_PER_BUFFER)
    print(data)
