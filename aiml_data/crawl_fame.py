import requests
from bs4 import BeautifulSoup
import urllib.parse
import xml.dom.minidom as minidom
class CelebrityCrawler(object):
    # 用于抓取百度百科中社会名流的基本信息
    def __init__(self,src_path = None):
        self.session = requests.Session()
        self.d = {}

        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        if src_path:
            with open(src_path,encoding='utf-8') as f:
                self.name_list = [name.strip() for name in f.readlines()]
        else:
            self.name_list = None
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
    def save_to_file(self,path='./aiml_data/celebrity.aiml'):
        template = '''
        <aiml version="1.0.1" encoding="UTF-8">
        '''
        doc = minidom.Document()
        root = doc.createElement('aiml')
        root.setAttribute('version','1.0.1')
        root.setAttribute('encoding','UTF-8')
        doc.appendChild(root)
        category = doc.createElement('category')
        root.appendChild(category)
        pattern = doc.createElement('pattern')
        pattern.appendChild(doc.createTextNode('谁是*'))
        template = doc.createElement('template')
        category.appendChild(pattern)
        category.appendChild(template)
        think = doc.createElement('think')
        set_ = doc.createElement('set')
        set_.setAttribute('name','star')
        star = doc.createElement('star')
        set_.appendChild(star)
        think.appendChild(set_)
        template.appendChild(think)
        condition = doc.createElement('condition')
        condition.setAttribute('name','star')
        template.appendChild(condition)
        for k,v in self.d.items():
            li = doc.createElement('li')
            li.setAttribute('value',k)
            text = doc.createTextNode(str(v))
            li.appendChild(text)
            condition.appendChild(li)
        li = doc.createElement('li')

        li.appendChild(doc.createTextNode("我跟"))
        li.appendChild(doc.createElement('star'))
        li.appendChild(doc.createTextNode("不熟"))
        condition.appendChild(li)

        with open(path,'w',encoding='utf-8') as f:
            doc.writexml(f, indent='', addindent='', newl='', encoding="utf-8")

    def run(self):
        for name in self.name_list:
            self.get_fame_to_dict(name)
        self.save_to_file()
        print('Done')


def main():
    cc = CelebrityCrawler(src_path=r'./aiml_data\name_list.txt')
    cc.run()

if __name__ == '__main__':
    main()
