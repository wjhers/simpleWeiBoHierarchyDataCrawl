#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Fixed by:wjher

'''
处理微博数据
1 名称处理为英文字符串
2 时间处理

'''

import os
import json
import string
import re
from zhon.hanzi import punctuation
from xpinyin import Pinyin
import random
random.seed(2022)

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQISTUVWXYZ0123456789"
def buildName(length:int):
    global alphabet
    characters = "".join(random.sample(alphabet, length))
    return characters

def load_json(filename):
    with open(filename, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)
    data = recursive(data)
    return data

def save_json(filename, savedata):
    outputFile = open(filename, "w", encoding='utf-8')
    json.dump(savedata, outputFile, ensure_ascii=False)
    outputFile.close()


def recursive(data:dict):
    # # name
    # data['name'] = en_name(data['name'], 0)
    # # source
    # data['data']['source'] = en_name(data['data']['source'], 0)
    # # time
    # # data['data']['time'] = data['data']['time'] #.split(' ')[0]
    # # id
    # # data['data']['nodeIndex'] = encodingIndex()
    # # 位置
    # data['data']['geo'] = encodingGeo()
    # # 性别
    # if(data['data']['gender'] == '-'):
    #     data['data']['gender'] = encodingGender()
    # # 长文本
    # data['data']['isLongText'] = encodingLongText()
    # # 文本长度
    # data['data']['textLength'] = random.randint(20,50) if data['data']['isLongText'] else random.randint(2,5)
    # # 用户类型
    # if data['data']['icon_list'] > 0:
    #     data['data']['type'] = 'vip'
    # else:
    #     data['data']['type'] = 'common'
    
    if data['data']['followers_count'] == 0:
        data['data']['followers_count'] = 3
        data['data']['followers_count_str'] = "3"

    # ============================================================ #
    # data['data']['verified'] = 0
    # data['data']['verified_type'] = -1
    # data['data']['domain'] = '-'
    # data['data']['mbrank'] = 1
    # data['data']['mbtype'] = 1
    # data['data']['icon_list'] = 0
    # data['data']['textLength'] = 0
    # data['data']['comments_count'] = 0
    # data['data']['attitudes_count'] = 0
    # data['data']['isLongText'] = 0
    # data['data']['is_show_bulletin'] = 0
    # data['data']['followers_count'] = 0
    # data['data']['followers_count_str'] = '0'
    # data['data']['friends_count'] = 0
    # data['data']['statuses_count'] = 1
    # data['data']['edu'] = '-'
    # data['data']['career'] = '-'
    # data['data']['type'] = 'common'
    # ============================================================ #


    
    if('children' in data.keys()) and len(data['children']):
        for element in data['children']:
            recursive(element)
    else:
        data['children'] = []
    
    return data


nodeIndex = -1
def encodingIndex():
    global nodeIndex
    nodeIndex = nodeIndex + 1
    return nodeIndex

def encodingGeo():
    provinces = ['Anhui','Beijing', 'Chongqing','Fujian','Gansu','Guangdong','Guangxi',
    'Guizhou','Hainan','Hebei','Henan','Heilongjiang','Hubei','Hunan','Jilin','Jiangsu',
    'Jiangxi','Liaoning','Inner Mongoria','Ningxia','Qinghai','Shangdong','Shanxi',
    'Shaanxi','Shanghai','Sichuan','Tianjin','Tibet','Xinjiang','Yunnan','Zhejiang',
    'Macao','Hong Kong','Taiwan']
    return random.choice(provinces)

def encodingGender():
    gender = ['m', 'f']
    return random.choice(gender)

def encodingLongText():
    return random.choice([0, 1])

def encodingTextLength():
    return random.randint(20,50)

Index = 0
def en_name(name:str, addIndex):
    global Index
    # Chinese Japanese
    name = re.sub('[{}]'.format(string.punctuation),"",name)
    name = re.sub('[{}]'.format(punctuation),"",name)
    name = re.sub('[\d]','',name)
    name = name.replace(' ','-')
    p = Pinyin()
    if addIndex:
        name = p.get_pinyin(name,'') + buildName(length=5) + str(Index)
        Index = Index + 1
    else:
        name = p.get_pinyin(name,'')
    
    return name



data = load_json('./LgQfNwnmY444.json')
save_json('./LgQfNwnmY444.json', savedata=data)