import aiml
from datetime import timedelta
from datetime import datetime
import locale

import os
from weather import WeatherHandler
class Dialogue(object):
    def __init__(self, aiml_data_dir = './aiml_data'):
        locale.setlocale(locale.LC_CTYPE,'chinese')
        self._brain = aiml.Kernel()
        pwd = os.curdir
        os.chdir(os.path.join(pwd,aiml_data_dir))
        self._brain.learn("std-startup.xml")
        self._brain.respond('load aiml b')
        os.chdir(pwd)
        self._task_handler={
            '天气':self._get_weather,
            '日期':self._get_date,
            '时间':self._get_time,
        }
    def _get_weather(self,*args):
        try:
            location = args[0]
        except:
            location = '杭州'
        wh = WeatherHandler()
        return wh.get_response(location)
    def _get_time(self,*args):
        now = datetime.now()
        result ='现在是'+now.strftime("%H点%M分")
        return result
    def _get_date(self,*args):

        try:
            interval =  args[0]
        except:
            interval = '今天'
        interval_map = {
            '前天':-2,
            '昨天':-1,
            '今天':0,
            '明天':1,
            '后天':2
        }
        delta = timedelta(days= interval_map.get(interval,0))
        result = (datetime.now()+delta).strftime("%Y年%m月%d日")
        return result


    def respond(self,sentence):
        aiml_rsp = self._brain.respond(sentence)
        if aiml_rsp[:4] == '实时查询':
            params = aiml_rsp.split()
            name = params[1]
            rsp = ''
            if name in self._task_handler:
                task_handler = self._task_handler[name]
            try:
                args = params[2:]
                rsp = task_handler(*args)
            except Exception as e:
                print(e)
                pass
            final_rsp = rsp
        else:
            final_rsp = aiml_rsp
        final_rsp = final_rsp or '我还小，你说的我还不懂'
        return final_rsp

def main():
    dlg = Dialogue()
    while True:
        input_ = input(">>>")
        rsp= dlg.respond(input_)
        print(rsp)



if __name__ == '__main__':
    main()
