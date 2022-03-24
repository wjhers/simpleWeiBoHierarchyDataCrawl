#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:wjher

import os
import json

def load_json(filename):
    with open(filename, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)
    return data

def save_json(filename, savedata):
    outputFile = open(filename, "w", encoding='utf-8')
    json.dump(savedata, outputFile, ensure_ascii=False)
    outputFile.close()

def addNode(parent, node):
    if node['pid'] == parent['mid'] or node['pid'] == '':
        node['pid'] = parent['mid']
        if 'children' not in parent.keys():
            parent['children'] = []
        parent['children'].append(node)
        return True
    else:
        if 'children' not in parent.keys():
            parent['children'] = []
        for child in parent['children']:
            if addNode(child, node):
                return True
    return False

def findParent(nodeList):
    ans = []
    for ele in nodeList:
        if('pid' not in ele):
            ans.append(ele)
    # print(len(ans))
    return ans[0]

def findChildren(nodeP, datalist):
    for ele in datalist:
        if ele['name'] != nodeP['name'] and ele['pid'] == nodeP['mid']:
            if 'children' not in nodeP.keys():
                nodeP['children'] = []
            nodeP['children'].append(ele)


def singledata2tree(sourcepath, targetpath):
    datalist = load_json(sourcepath)
    root = findParent(datalist)
    # root = datalist[0]
    for node in datalist:
        if node['name'] != root['name']:
            addNode(root, node)
    save_json(targetpath, root)



source = './repost3'
listdir = os.listdir(source)


for path in listdir:
    print(source + '/' + path)
    singledata2tree(source + '/' + path, './repost4' + '/' + path)