#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:wjher

# import jsons
# import pandas as pd

# df = pd.read_csv('./hotlinks/link.csv')
# ansList = df['hotlink'].values.tolist()
# print(ansList)


# def load_json(filename):
#     with open(filename, 'r', encoding='UTF-8') as json_file:
#         data = json.load(json_file)
#     return data

# def save_json(filename, savedata):
#     outputFile = open(filename, "w", encoding='utf-8')
#     json.dump(savedata, outputFile, ensure_ascii=False)
#     outputFile.close()

# def addNode(parent, node):
#     if node['pid'] == parent['mid'] or node['pid'] == '':
#         node['pid'] = parent['mid']
#         if 'children' not in parent.keys():
#             parent['children'] = []
#         parent['children'].append(node)
#         return True
#     else:
#         for child in parent['children']:
#             if addNode(child, node):
#                 return True
#     return False


# datalist = load_json('./repost/6.json')
# root = datalist[0]
# for node in datalist[1:]:
#     addNode(root, node)
# save_json('./tmp.json',root)
