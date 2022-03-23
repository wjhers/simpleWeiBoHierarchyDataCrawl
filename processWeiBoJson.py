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
    data['name'] = en_name(data['name'], 0)
    data['data']['source'] = en_name(data['data']['source'], 0)
    # 生成唯一的节点id索引
    data['data']['nodeIndex'] = encodingIndex()
    data['data']['geo'] = encodingGeo()
    if('children' in data.keys()) and len(data['children']):
        for element in data['children']:
            recursive(element)
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
    # pass

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



data = load_json('./LkBSYdhE3235_1.json')
save_json('./LkBSYdhE3235_2.json', savedata=data)