import requests
import os
class WeatherHandler(object):
    def __init__(self, *args, **kwargs):
        self.location = ''
        self.token = 'unGcwcjM4VR7oPEd'
        pwd = os.path.abspath(os.curdir)
        os.chdir(os.path.join(pwd,'/weather.txt'))
        with open(r'./weather.txt',encoding='utf8') as f:
            # 地点:api
            self.api_dict = dict(line.strip().split(' || ')[1::2]for line in f.readlines())
        os.chdir(pwd)

    def get_response(self,location):
        '''
        args:
            location: str
        return:
            response
        '''


        if location in self.api_dict:
            response = self.request_data(location)
        else:
            response = '暂不支持'

        return response

    def request_data(self,location):
        try:
            url = self.api_dict[location].replace('YOUR_TOKEN',self.token)
        except KeyError:
            return None
        rsp = requests.get(url)
        description = rsp.json()['result']['hourly']['description']
        return description


def main():
    wh = WeatherHandler()
    print(wh.get_response(*['温州']))

if __name__ == '__main__':
    main()
