import pyaudio
import wave
import os
import sys
from aip import AipSpeech
import dialogue
import speech_part

USE_PYAUDIO = False
class ChatBot:

    _AUDIO_DIR = './audio.pcm'
    _RESPONSE_DIR = './rsp.mp3'
    def __init__(self, *args, **kwargs):
        self.CLIENT =speech_part.SpeechClient()
    def run(self):
        while True:
            # 录音
            print('start record')
            self.record_audio()
            print('stop record')
            # 读取
            audio_buffer = self.read_audio()
            # 识别
            try:
                msg = self.recognize_audio(audio_buffer)
            except speech_part.RecognizeError as e:
                response = str(e)
            else:
                # 获取回复
                response = dialogue.generate_response(msg)
            # 语音合成
            try:
                response_buff = self.compose_audio(text=response)
            except speech_part.ComposeError as e:
                print(e)
            else:
                speech_part.save_mp3(response_buff,self._RESPONSE_DIR)
                self.play_audio()



        # 输入 - 输出
        # response = self.DIALOGUE.get_response(text)

    def record_audio(self,time=5,path = _AUDIO_DIR):
        os.system ('arecord -r 44100 -f s16_le -c 1 -t raw -D "plughw:1,0" -d {time} {path}'.format(path=(path+'.origin'),time=time))
        # 录音格式转换
        os.system('ffmpeg -y -f s16le -ac 1 -ar 44100 -i {src_path} -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {dst_path}'.format(src_path=(path+'.origin'),dst_path=path))

    def read_audio(self,path =_AUDIO_DIR):
        with open(path,'rb') as audio:
            buffer = audio.read()
            return buffer

    def recognize_audio(self,buffer):
        self.CLIENT.speech_recognize(speech=buffer,audio_type='pcm')

    def compose_audio(self,text='我是一头猪呀'):
        result = self.CLIENT.speech_compose(text)
        if not isinstance(result,dict):
            with open(self._RESPONSE_DIR, 'wb') as f:
                f.write(result)

    def play_audio(self,path=_RESPONSE_DIR):
        os.system('mpg123 {path}')


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


