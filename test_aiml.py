# -*- coding: utf-8 -*-
import aiml
import sys
import os

def get_module_dir(name):
    path = getattr(sys.modules[name], '__file__', None)
    if not path:
        raise AttributeError('module %s has not attribute __file__' % name)
    return os.path.dirname(os.path.abspath(path))


alice_path = os.curdir + '/aiml_data'

#切换到语料库所在工作目录
os.chdir(alice_path)

alice = aiml.Kernel()
alice.learn("std-startup.xml")
alice.respond('load aiml b')
alice.respond('init')

while True:
    input_ = input("Enter your message >> ")
    # input_ = '聊点什么吧'
    rsp = alice.respond(input_)
    print(rsp)
