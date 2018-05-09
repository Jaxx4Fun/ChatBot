import pyaudio
import wave
import os
import sys
from aip import AipSpeech
class ChatBot:
    def __init__(self, *args, **kwargs):
        self.CLIENT =AipSpeech(
            appId = '10528707',
            apiKey = 'iBCuQlT14vkiPzr2qzEYpu6s',
            secretKey = '7znifePL2YhGeKgqSsw2Q33sXqsIG6x2'
        )
        self.AUDIO_DIR = './audio.wav'
        self.RESPONSE_DIR = './rsp.mp3'
    def run(self):
        audio_data = self.record_audio()

        text = self.recognize_audio(audio_data)
        # 输入 - 输出
        # response = self.DIALOGUE.get_response(text)

    def record_audio(self,time=5):
        os.system ('arecord -D "plughw:1,0" -d 10 {dir}'.format(dir=self.AUDIO_DIR))
        with open(self.AUDIO_DIR) as audio:
            buffer = audio.read()
            return buffer
    def recognize_audio(self,buffer):
        self.CLIENT.asr(speech=buffer,format='wav',rate=16000)


    def compose_audio(self,text_data='我是一头猪呀'):
        result = self.CLIENT.synthesis(text_data)
        if not isinstance(result,dict):
            with open(self.RESPONSE_DIR, 'wb') as f:
                f.write(result)

    def play_audio(self):
        if os.path.exists(self.RESPONSE_DIR):
            os.system('aplay %s'%self.RESPONSE_DIR)


    def record_audio_by_pa(self):

        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("recording...")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("done")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__ == '__main__':
    cb = ChatBot()
    # test compose
    cb.run()


