import requests
import json
class Tuling(object):

    _URL_V1 = 'http://www.tuling123.com/openapi/api'
    _URL_V2 = 'http://openapi.tuling123.com/openapi/api/v2'
    _API_KEY = 'da92afb705364f098ed908155956ecba'
    _USE_V1 = False
    def respond(self,sentence):
        if self._USE_V1:
            d = {
                'key': self._API_KEY,
                'info': sentence,
                'userid': '0'
            }
            rsp = requests.post(self._URL_V1,data=json.dumps(d))
            try:
                result = rsp.json()['text']
            except:
                result = ''
            return result
        else:
            d = {
                "reqType":0,
                "perception": {
                    "inputText": {
                        "text": sentence
                    }
                },
                "userInfo": {
                    "apiKey": self._API_KEY,
                    "userId": "0"
                }
            }
            json_data = json.dumps(d)
            rsp = requests.post(self._URL_V2,data=json_data)
            try:
                result = rsp.json()['results'][0]['values']['text']
            except:
                result = ''
            return result

def main():
    t = Tuling()
    print(t.respond('你能干什么'))

if __name__ == '__main__':
    main()

