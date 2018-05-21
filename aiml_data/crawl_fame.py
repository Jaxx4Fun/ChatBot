import requests
from bs4 import BeautifulSoup
import urllib.parse
from multiprocessing import pool
class CelebrityCrawler(object):
    # 用于抓取百度百科中社会名流的基本信息
    def __init__(self,file_path = None):
        self.session = requests.Session()
        self.d = {}
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        if file_path:
            with open(file_path,encoding='utf-8') as f:
                self.name_list = [name.strip() for name in f.readlines()]
    def get_fame_by_name(self,name):
        name = urllib.parse.quote(name)
        url = "https://baike.baidu.com/item/"+name

        rsp = self.session.get(url)
        rsp.encoding = 'utf-8'
        description = self.extract_page(rsp)
        return description
    def extract_page(self,rsp):
        bs = BeautifulSoup(rsp.text,'html.parser')
        first_para = bs.find(class_='lemma-summary').find('div')
        return first_para.text
    def get_fame_to_dict(self,name):
        print('正在抓取'+name)
        desc = self.get_fame_by_name(name)
        self.d[name] = desc
        print(name+"抓取完毕")
    def save_to_file(self,path='celebrity.aiml'):
        template = '''
        <aiml version="1.0.1" encoding="UTF-8">
        '''
        for k,v in self.d.items():
            category = '''
                    <category>
                    <pattern>谁是{name}</pattern>
                    <template>{description}
                    </template>
                </category>
                '''.format(name=k,description=v)
            template += category
        template += '</aiml>'
        with open(path,'w',encoding='utf-8') as f:
            f.write(template)

    def run(self):
        p = pool.Pool(4)
        for name in self.name_list:
            self.get_fame_to_dict(name)
        self.save_to_file()
        print('Done')


def main():
    cc = CelebrityCrawler(file_path=r'C:\Users\DELL\Desktop\毕设2\ChatBot\aiml_data\name_list.txt')
    print(cc.run())

if __name__ == '__main__':
    main()
