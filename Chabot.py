import pyaudio
import wave
import os
import sys
import speech_part
import logging
import new_dialogue
#初始化logger
logger = logging.getLogger(__name__)
# 配置日志级别，如果不显示配置，默认为Warning，表示所有warning级别已下的其他level直接被省略，
# 内部绑定的handler对象也只能接收到warning级别以上的level，你可以理解为总开关
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                datefmt="%m/%d/%Y %I:%M:%S %p")  # 创建一个格式化对象
info_file = logging.FileHandler('./log/chatbot/info.log')
debug_file = logging.FileHandler('./log/chatbot/debug.log')
debug_file.setLevel(logging.DEBUG)
console = logging.StreamHandler() # 配置日志输出到控制台
console.setLevel(logging.INFO) # 设置输出到控制台的最低日志级别
console.setFormatter(formatter)  # 设置格式
logger.addHandler(console)
logger.addHandler(info_file)
logger.addHandler(debug_file)
class ChatBot:
    # 预先的定义好音频参数和录音时间
    _AUDIO_DIR = './audio.pcm'
    _AUDIO_RATE = 44100
    _AUDIO_CHANNEL = 1
    _AUDIO16_DIR = './audio16.pcm'
    _AUDIO16_CHANNEL = 1
    _AUDIO16_RATE = 16000
    _RESPONSE_DIR = './rsp.mp3'
    _DEFAULT_RECORD_TIME = 5

    def __init__(self, *args, **kwargs):
        logger.info('ChatBot初始化')
        self.CLIENT =speech_part.SpeechClient()
        self.BRAIN = new_dialogue.Dialogue()

    def run(self):
        while True:
            # 录音
            logger.info('开始录音')
            #TODO 这里要加个嘟？
            audio_buffer = self.record_audio()
            logger.info('录音结束')
            # 读取
            # audio_buffer = open('./audio16.pcm','rb').read()
            # 识别
            try:
                msg = self.recognize_audio(audio_buffer)
                logger.info('Recognize Result:'+msg)
            except speech_part.RecognizeError as e:
                logger.error('Recognize Error',exc_info=True)
                response = str(e)
            else:
                # 获取回复
                response = self.BRAIN.respond(msg)
                logger.info('Dialogue Result:'+response)
            # 语音合成
            try:
                response_buff = self.compose_audio(text=response)
            except speech_part.ComposeError as e:
                logger.error('compose error',exc_info=True)
            else:
                speech_part.save_mp3(response_buff,self._RESPONSE_DIR)
                self.play_audio()



        # 输入 - 输出
        # response = self.DIALOGUE.get_response(text)

    def record_audio(self,time=_DEFAULT_RECORD_TIME):
        buffer = b''
        if 'posix' in os.name:
            os.system ('arecord -r {rate} -f s16_le -c {channel} -t raw -D "plughw:1,0" -d {time} {path}'.format(path=(self._AUDIO_DIR+'.origin'),
                time=time,
                rate=self._AUDIO_RATE,
                channel=self._AUDIO_CHANNEL))
            # 录音格式转换
            os.system('ffmpeg -y -f s16le -ac {src_channel} -ar {src_rate} -i {src_path} -acodec pcm_s16le -f s16le -ac {dst_channel} -ar {dst_rate} {dst_path}'.format(
                src_path=(self._AUDIO_DIR+'.origin'),
                src_rate=self._AUDIO_RATE,
                src_channel = self._AUDIO_CHANNEL,
                dst_path=self._AUDIO16_DIR,
                dst_rate=self._AUDIO16_RATE,
                dst_channel=self._AUDIO16_CHANNEL))
            with open(self._AUDIO16_DIR,'rb') as f:
                buffer =  f.read()
        else:
            buffer = self.record_audio_by_pa()
        return buffer


    def read_audio(self,path =_AUDIO_DIR):
        with open(path,'rb') as audio:
            buffer = audio.read()
            return buffer

    def recognize_audio(self,buffer):
        return self.CLIENT.speech_recognize(speech=buffer,audio_type='pcm')

    def compose_audio(self,text='我是一头猪呀'):
        result = self.CLIENT.speech_compose(text)
        return result

    def play_audio(self,path=_RESPONSE_DIR):
        os.system('mpg123 {path}'.format(path=path))


    def record_audio_by_pa(self):

        CHUNK = 512
        FORMAT = pyaudio.paInt16
        CHANNELS = self._AUDIO16_CHANNEL
        RATE = self._AUDIO16_RATE
        RECORD_SECONDS = self._DEFAULT_RECORD_TIME
        WAVE_OUTPUT_FILENAME = "output.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        logger.info("使用pyaudio开始录音")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        logger.info("录音结束")

        stream.stop_stream()
        stream.close()
        p.terminate()
        buffer = b''.join(frames)
        return buffer

        # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        # wf.setnchannels(CHANNELS)
        # wf.setsampwidth(p.get_sample_size(FORMAT))
        # wf.setframerate(RATE)
        # wf.writeframes(b''.join(frames))
        # wf.close()


if __name__ == '__main__':
    cb = ChatBot()
    # test compose

    cb.run()


