import os
import time
import speech_part
try:
    import RPi.GPIO as GPIO
except :
    pass
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.IN)
except:
    pass
t = 0
client = speech_part.SpeechClient()
def cost_time(func):
    def wrapper(*args,**kw):
        s = time.time()
        new = func(*args,**kw)
        print("%.2f"%(time.time()-s))
        return new
    return wrapper
@cost_time
def a():
    print(1)
@cost_time
def record():
    for i in range(20):
        # 停止录音
        if not GPIO.input(17):
            t = i
            break
        cmd = 'arecord -r 44100 -f s16_le -c 1\
            -t raw -D "plughw:1,0" -d 1 \
            temp/{name}'.format(name=('a'+str(i)))
        os.system(cmd)

def try_rec():
    buff = b''
    for i in range(t):
        with open('temp/a'+str(i),'rb') as f:
            buff += f.read()
    rsp = client.speech_recognize(buff)
    print(rsp)


def main():
    record()
    try_rec()

if __name__ == '__main__':
    main()
