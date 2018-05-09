import pyaudio
from pyaudio import paInt16
import wave
import numpy as np
# from matplotlib import pyplot as plt
# use pyaudio
RATE = 44100
FORMAT = paInt16
CHANNELS = 1
FRAMES_PER_BUFFER = 1024
CHUNK = 512
TIME = 5
pa = pyaudio.PyAudio()
stream = pa.open(rate=RATE,
                format=FORMAT,
                channels=CHANNELS,
                frames_per_buffer=FRAMES_PER_BUFFER,
                input=True)
buffer = []
for i in range(RATE*TIME//CHUNK):
    print('CHUNK %s :\n'.ljust(15,'-')% i)
    try:
        data = stream.read(CHUNK)
    except OSError:
        stream = pa.open(rate=RATE,
                        format=FORMAT,
                        channels=CHANNELS,
                        frames_per_buffer=FRAMES_PER_BUFFER,
                        input=True)
        data = stream.read(CHUNK)

    buffer.append(np.fromstring(data,dtype=np.short))
buff =np.array(buffer).reshape((-1,))
with open('./audio_bin.txt','xb') as f:
    f.write(buff)

# plt.plot(buff)
# plt.show()
# # use arecord
# import os
# os.system('arecord -d 10 ')
