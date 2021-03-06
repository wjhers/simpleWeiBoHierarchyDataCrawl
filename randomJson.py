#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:wjher

# 实时可视化层次结构数据
# https://observablehq.com/@katopz/ml-map-on-d3-tidy-tree

import json
import random
from addJsonValue import addJsonValue

def buildName(length:int):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQISTUVWXYZ0123456789"
    tmpname = "".join(random.sample(alphabet, length))
    return tmpname

def buildInitDict(name, depth):
    return {"name":name, "pid":depth - 1 if depth > 0 else depth, "mid":depth, "children":[]}

def addInitNode(parent, node):
    if node['pid'] == parent['mid'] or node['pid'] == '':
        node['pid'] = parent['mid']
        if 'children' not in parent.keys():
            parent['children'] = []
        # parent['children'].append(node)
        # 添加元素
        tmp_len = 0 if len(parent['children'])==0 else len(parent['children']) - 1
        parent['children'].insert(random.randint(0, tmp_len),node)
        return True
    else:
        if 'children' not in parent.keys():
            parent['children'] = []
        for child in parent['children']:
            if addInitNode(child, node):
                return True
    return False

def initJson(depth, nameList):
    init_nameList = random.sample(nameList, depth+1)
    root = buildInitDict(init_nameList[0], 0)
    init_nameDictList = []
    for i in range(len(init_nameList)):
        init_nameDictList.append(buildInitDict(init_nameList[i], i))
    root = init_nameDictList[0]
    for node in init_nameDictList[1:]:
        addInitNode(root, node)
    return init_nameList, root

def buildOtherDict(name, parentname):
    return {"name":name, "pid":parentname, "children":[]}


def addOtherNode(parent, node, depth):
    if node['pid'] == parent['name'] and parent['mid']+1 <= depth:
        node['pid'] = parent['mid']
        # mid: level of the current node
        node['mid'] = parent['mid'] + 1
        if 'children' not in parent.keys():
            parent['children'] = []
        # 添加元素
        # if(random.random()<=0.5):
            # 列表末尾添加
            # parent['children'].append(node)
        # else:
            # 列表随机一个位置添加
            # tmp_len = 0 if len(parent['children'])==0 else  len(parent['children']) - 1
            # parent['children'].insert(random.randint(0, tmp_len),node)
        tmp_len = 0 if len(parent['children'])==0 else  len(parent['children']) - 1
        parent['children'].insert(random.randint(0, tmp_len),node)
        return True
    else:
        if 'children' not in parent.keys():
            parent['children'] = []
        for child in parent['children']:
            if addOtherNode(child, node, depth):
                return True
    return False


def save_json(filename, savedata):
    outputFile = open(filename, "w", encoding='utf-8')
    json.dump(savedata, outputFile, ensure_ascii=False)
    outputFile.close()

def randomJson(namelen, depth, nodesize):

    nameList = list(set([buildName(length=namelen) for i in range(nodesize)]))

    init_nameList, root = initJson(depth, nameList=nameList)
    rootname = init_nameList[0]

    other_nameList = list(set(nameList) - set(init_nameList))

    for el in other_nameList:
        if(el not in init_nameList):
            parentname = random.choice(init_nameList)
            node  = buildOtherDict(el, parentname)
            while(not addOtherNode(root, node, depth)):
                parentname = random.choice(init_nameList)
                node  = buildOtherDict(el, parentname)
            init_nameList += [el]
    
    return root, rootname

# 随机生成10条数据 高度2-6 节点名称长度5-15 节点个数20-120 命名方式为 根节点名称+深度.json

for i in range(10):
    depth = random.randint(4, 6)
    namelength = random.randint(5, 10)
    nodesize = random.randint(40, 120)
    root, rootname = randomJson(namelen=namelength, depth=depth, nodesize=nodesize)
    filename = './randjson/'+rootname+"_"+str(depth)+"_"+str(nodesize)+ '.json'
    save_json(filename=filename, savedata=root)


source = './randjson'
addJsonValue(source=source)

