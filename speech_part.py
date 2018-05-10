import aip
class SpeechClient(object):
    _CLIENT = aip.AipSpeech(
                appId = '10528707',
                apiKey = 'iBCuQlT14vkiPzr2qzEYpu6s',
                secretKey = '7znifePL2YhGeKgqSsw2Q33sXqsIG6x2'
            )

    _DEFAULT_RATE=16000

    _DEFAULT_AUDIO_TYPE='pcm'

    _DEFAULT_AUDIO_OPTION = {
        'spd':5,
        'vol':5,
        'pit':5,
        'per':1
    }
    def speech_recognize(self,
                        speech,
                        audio_type=_DEFAULT_AUDIO_TYPE,
                        rate=_DEFAULT_RATE):
        result = self._CLIENT.asr(speech=speech,
                                format=audio_type,
                                rate=rate)
        if result and result.get('err_no') == 0:
            return result.get('result')
        else:
            raise Exception(result)

    def speech_compose(self,response='测试数据：你好猪头肉'):
        result = self._CLIENT.synthesis(text=response,options=self._DEFAULT_AUDIO_OPTION)
        if isinstance(result,bytes):
            return result
        elif isinstance(result,dict):
            raise Exception(result)

def convert_mp3_to_pcm(original_path,new_path):
    import os
    os.system('ffmpeg -y  -i {original}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {new}'.
                format(original=original_path,new=new_path))

def save_mp3(data,path):
    with open(path,'wb') as f:
        f.write(data)

def read_pcm(path):
    with open(path,'rb') as f:
        return f.read()

def main():
    mp3_path = './rsp.mp3'
    pcm_path = './rsp.pcm'
    sc = SpeechClient()
    buff = sc.speech_compose()
    save_mp3(buff,mp3_path)
    convert_mp3_to_pcm(mp3_path,pcm_path)
    buff = read_pcm(pcm_path)

    print('Test Done',sc.speech_recognize(buff,audio_type='pcm'))
if __name__ == '__main__':
    main()
