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


def singledata2tree(sourcepath, targetpath):
    datalist = load_json(sourcepath)
    root = datalist[0]
    for node in datalist[1:]:
        addNode(root, node)
    save_json(targetpath, root)



source = './repost'
listdir = os.listdir(source)


for path in listdir:
    # print(source + '/' + path)
    singledata2tree(source + '/' + path, source + '/' + path)