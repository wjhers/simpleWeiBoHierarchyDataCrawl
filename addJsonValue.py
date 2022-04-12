#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Fixed by:wjher

'''
处理 json 统一格式为 {"name":namestr, "children":[{"name":namestr, "value":value}]}
同时 只有叶子节点具有value值

'''

import os
import json
import string
import re
from zhon.hanzi import punctuation
from xpinyin import Pinyin
# from pykakasi import kakasi, wakati
import random
# random.seed(2022)


def load_json(filename,str_to_value:str='value'):
    with open(filename, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)
    data = recursive(data, str_to_value)
    return data

def save_json(filename, savedata):
    outputFile = open(filename, "w", encoding='utf-8')
    json.dump(savedata, outputFile, ensure_ascii=False)
    outputFile.close()

def recursive(data:dict, str_to_value:str='value'):
    ans = {}
    ans['name'] = en_name(data['name'])
    if('children' in data.keys()) and len(data['children']):
        ans['children'] = []
        for element in data['children']:
            ans1 = recursive(element,str_to_value)
            ans['children'].append(ans1)
    else:
        if(str_to_value in data.keys()):
            ans['value'] = random_value() #int(data[str_to_value]) if (int(data[str_to_value]) > 1 and int(data[str_to_value]) < 100) else random_value()
        else:
            ans['value'] = random_value()
    return ans


def en_name(name:str):
    # Chinese Japanese
    name = re.sub('[{}]'.format(string.punctuation),"",name)
    name = re.sub('[{}]'.format(punctuation),"",name)
    name = re.sub('[\d]','',name)
    name = name.replace(' ','-')
    p = Pinyin()
    name = p.get_pinyin(name,'')
    # kks = kakasi()
    # kks.setMode('H','a')
    # kks.setMode('K','a')
    # kks.setMode('J','a')
    # kks.setMode('r','Hepburn')
    # kks.setMode('s',True)
    # kks.setMode('c',True)
    # conv = kks.getConverter()
    # name = conv.do(name)
    
    return name

def random_value():
    value_a = random.gauss(0,1)
    value_b = random.randint(10, 100)
    return int(value_a * value_b) if (int(value_a * value_b) > 1 and int(value_a * value_b) < 100) else random.randint(10, 30)


def addJsonValue(source):
    listdir = os.listdir(source)
    for path in listdir:
        data = load_json(filename=source + '/' + path, str_to_value='value')
        save_json(filename=source + '/' + path, savedata=data)

source = './randjson'
addJsonValue(source=source)