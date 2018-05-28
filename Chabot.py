import pyaudio
import wave
import os
import sys
import speech_part
import logging
import new_dialogue
try:
    import RPi.GPIO as GPIO
except:
    pass
#初始化logger
logger = logging.getLogger(__name__)
# 配置日志级别，如果不显示配置，默认为Warning，表示所有warning级别已下的其他level直接被省略，
# 内部绑定的handler对象也只能接收到warning级别以上的level，你可以理解为总开关
logger.setLevel(logging.INFO)
default_formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
                                datefmt="%m/%d/%Y %I:%M:%S %p")  # 创建一个格式化对象
info_file = logging.FileHandler('./log/chatbot/info.log')
debug_file = logging.FileHandler('./log/chatbot/debug.log')
debug_file.setLevel(logging.DEBUG)
info_file.setFormatter(default_formatter)
debug_file.setFormatter(default_formatter)
console = logging.StreamHandler() # 配置日志输出到控制台
console.setLevel(logging.INFO) # 设置输出到控制台的最低日志级别
console.setFormatter(default_formatter)  # 设置格式
logger.addHandler(console)
logger.addHandler(info_file)
logger.addHandler(debug_file)
# 聊天记录的logger
history_logger = logging.getLogger(__name__+'.history')
history_logger.setLevel(logging.DEBUG)
history_formatter = logging.Formatter(fmt="%(asctime)s - %(message)s")
history_handler = logging.FileHandler('./log/chatbot/history.log')
history_handler.setFormatter(history_formatter)
history_logger.addHandler(history_handler)
sys.modules[__name__]
BASE_DIR = getattr(sys.modules[__name__],'__file__',None)
if BASE_DIR:
    BASE_DIR = os.path.dirname(os.path.abspath(BASE_DIR))
else:
    BASE_DIR = '/home/pi/ChatBot'
os.chdir(BASE_DIR)
class ChatBot:
    # 预先的定义好音频参数和录音时间
    _AUDIO_DIR = './temp/audio.pcm'
    _AUDIO_RATE = 44100
    _AUDIO_CHANNEL = 1
    _AUDIO16_DIR = './temp/audio16.pcm'
    _AUDIO16_CHANNEL = 1
    _AUDIO16_RATE = 16000
    _RESPONSE_DIR = './temp/rsp.mp3'
    _DEFAULT_RECORD_TIME = 5
    _DINGDONG_DIR = './dingdong.mp3'

    def __init__(self, *args, **kwargs):
        logger.info('ChatBot初始化')
        self.CLIENT =speech_part.SpeechClient()
        self.BRAIN = new_dialogue.Dialogue()
        logger.info('树莓派按钮初始化')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.IN)


    def run(self):
        while True:
            #TODO 这里要加个嘟？或者按钮触发5秒录音
            try:
                while not GPIO.input(17):
                    pass
            except:
                pass
            # 录音
            logger.debug('开始录音')
            # 叮咚提示音
            self.play_audio(self._DINGDONG_DIR)
            audio_buffer = self.record_audio()
            logger.info('录音结束')
            # 读取
            # audio_buffer = open('./audio16.pcm','rb').read()
            # 识别
            try:
                msg = self.recognize_audio(audio_buffer)
                history_logger.info('User : '+msg)
            except speech_part.RecognizeError as e:
                history_logger.info('User : '+'（未能识别）')
                logger.error('Recognize Error',exc_info=True)
                response = str(e)
            else:
                # 获取回复
                response = self.BRAIN.respond(msg)
            # 回复作为聊天记录
            history_logger.info('Bot : '+response)

            try:
                # 语音合成
                response_buff = self.compose_audio(text=response)
            except speech_part.ComposeError as e:
                logger.error('Compose Error',exc_info=True)
            else:
                speech_part.save_mp3(response_buff,self._RESPONSE_DIR)
                self.play_audio()



        # 输入 - 输出
        # response = self.DIALOGUE.get_response(text)

    def record_audio(self,time=_DEFAULT_RECORD_TIME):
        buffer = b''
        if 'posix' in os.name:
            os.system ('arecord -r {rate} -f s16_le -c {channel}\
             -t raw -D "plughw:1,0" -d {time} \
             {path}'.format(path=(self._AUDIO_DIR+'.origin'),
                time=time,
                rate=self._AUDIO_RATE,
                channel=self._AUDIO_CHANNEL))
            # 录音格式转换
            os.system('ffmpeg -y -f s16le -ac {src_channel} \
            -ar {src_rate} -i {src_path} -acodec pcm_s16le -f s16le\
             -ac {dst_channel} -ar {dst_rate} {dst_path}'.format(
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


if __name__ == '__main__':
    cb = ChatBot()
    # test compose

    cb.run()


