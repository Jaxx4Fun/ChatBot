import pyaudio
from pyaudio import paInt16
import wave
import numpy as np
from matplotlib import pyplot as plt
# use pyaudio
RATE = 16000
FORMAT = paInt16
CHANNELS = 1
FRAMES_PER_BUFFER = 1024
pa = pyaudio.PyAudio()
stream = pa.open(rate=RATE,
                format=FORMAT,
                channels=CHANNELS,
                input=True)
for i in range(10):
    print('time %s \n:'% i)
    data = stream.read(FRAMES_PER_BUFFER)
    voice = np.fromstring(data,dtype=np.short)
    plt.plot(voice)
    plt.show()

    print(voice)
    print(len(voice))

# # use arecord
# import os
# os.system('arecord -d 10 ')
