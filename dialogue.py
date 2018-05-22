import rulebase
import random
import jieba
import jieba.analyse
import weather
def generate_response(msg):
    if '你好' == msg:
        rsp = '我有点难过'
    else:
        rsp = '这是一条测试回复'
    return rsp


class Dialogue(object):
    def __init__(self, stopword_path,word2vec_model_path,rule_dir):
        self.name = '猪头肉'
        self.last_sentence = ''
        self.current_domain = ''

        # 添加支持的任务，现有：天气查询
        self.support_task = {
            '天气':weather.WeatherHandler(),
        }


        self.rule_base = rulebase.RuleBase()
        self.rule_base.load_rules_files(rule_dir)
        # 5self.rule_base.load_model(word2vec_model_path)
        self.default_responses = [
            '我还不太理解你的意思'
        ]
        try:
            with open(stopword_path) as f:
                self.stopwords = f.read().split()
        except:
            self.stopwords =[]
        # 指示某些特定任务是否结束
        self.is_task_finished = True
        # 初始化jieba分词
        jieba.initialize()

        self.task_handler = None
    def get_response(self,sentence,threshold=0):
        # 判断是否是task
        # 如果任务对话尚未结束

        # domain match
        segment = self.segment_words(sentence)
        result_list,domain_links = self.rule_base.match(segment)

        # 有匹配的domain
        if result_list:
            top_result = result_list[0]
            top_similarity = top_result[0]
            top_domain = top_result[1]
            if top_domain in self.support_task:
                response=self.support_task[top_domain].get_response(segment)
            else:
                response = self.rule_base.get_response_by_domain(top_domain)

        response = response or random.choice(self.default_responses)

        return response

    def _get_domain_response(self,domain):
        return self.rule_base.rules[domain]['response']

    def segment_words(self,sentence):
        return [word for word in jieba.cut(sentence) if word not in self.stopwords]

def main():
    d = Dialogue(stopword_path='',word2vec_model_path=r'C:\Users\DELL\Desktop\Chatbot\Chatbot\model\model.bin',rule_dir=r'C:\Users\DELL\Desktop\Chatbot\Chatbot\RuleMatcher\rule')
    while True:
        speech = input('请输入\n')
        rsp = d.get_response(speech,threshold=0.4)
        print(rsp)

if __name__ == '__main__':
    main()
