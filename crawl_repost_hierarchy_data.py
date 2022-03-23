#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Fixed by:wjher
# reference: https://blog.csdn.net/HandsomeFishman
# 2022/03/23

import requests
from urllib.parse import urlencode
import json
import random
import os
import re
import time
import random
import datetime
import pandas as pd
from queue import Queue
from crawl_HotPoints_Links import get_repost_1

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X
    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
      rem = num % base
      num = num // base
      arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
      power = (strlen - (idx + 1))
      num += alphabet.index(char) * (base ** power)
      idx += 1
 
    return num

def mid_to_url(midint):

    # >>> mid_to_url(3501756485200075)
    # 'z0JH2lOMb'
    
    midint = str(midint)[::-1]
    size = len(midint) / 7 if len(midint) % 7 == 0 else len(midint) / 7 + 1
    result = []

    for i in range(int(size)):
      s = midint[i * 7: (i + 1) * 7][::-1]
      s = base62_encode(int(s))
      s_len = len(s)
      if i < size - 1 and len(s) < 4:
          s = '0' * (4 - s_len) + s
      result.append(s)
    
    result.reverse()
    return ''.join(result)

def url_to_mid(url):

    # >> url_to_mid('z0JH2lOMb')
    # 3501756485200075L

    url = str(url)[::-1]
    size = len(url) / 4 if len(url) % 4 == 0 else len(url) / 4 + 1
    result = []
    for i in range(int(size)):
      s = url[i * 4: (i + 1) * 4][::-1]
      s = str(base62_decode(str(s)))
      s_len = len(s)
      if i < size - 1 and s_len < 7:
          s = (7 - s_len) * '0' + s
      result.append(s)
    
    result.reverse()
    return str(int(''.join(result)))

def clean(weibos):
  # weibo 去重，a -> b ->c
  midset = set()
  index = len(weibos) - 1
  new_weibos = []
  while index >= 0:
    if not weibos[index]['mid'] in midset:
      midset.add(weibos[index]['mid'])
      new_weibos.append(weibos[index])
    index = index - 1
  return new_weibos

def formatTime(timeStr):
  GMT_FORMAT = "%a %b %d %H:%M:%S +0800 %Y"
  timeArray = datetime.datetime.strptime(timeStr, GMT_FORMAT)
  return timeArray.strftime("%Y-%m-%d %H:%M:%S")
    
def removeHyperlinks(text):
  return re.sub(r'<[Aa]\s+(.*?\s+)*?href\s*=\s*().+?\2(\s+.*?\s*)*?>.+?</[Aa]>', '', text, flags=re.MULTILINE)

def getLongText(mid, headers):
  text_url = "https://weibo.com/ajax/statuses/longtext?id=" + mid
  try:
    response = requests.get(url = text_url, headers = headers)
    if response.status_code == 200:
      return response.json().get('data').get('longTextContent')
  except requests.ConnectionError as e:
    print('Error', e.args, flush = True)
  return None

def getUserInfo(uid, headers):
  text_url = "https://weibo.com/ajax/profile/info?uid=" + str(uid)
  try:
    response = requests.get(url = text_url, headers = headers)
    if response.status_code == 200:
      return response.json().get('data')
  except requests.ConnectionError as e:
    print('Error', e.args, flush = True)
  return None

def getUserDetail(uid, headers):
  text_url = "https://weibo.com/ajax/profile/detail?uid=" + str(uid)
  try:
    response = requests.get(url = text_url, headers = headers)
    if response.status_code == 200:
      return response.json().get('data')
  except requests.ConnectionError as e:
    print('Error', e.args, flush = True)
  return None

def reponseInfo2Dict(mid, uid, mblog):
  weibo = {}
  data_w = {}
  data_w['visible_type'] = mblog.get('visible').get('type')
  data_w['visible_list_id'] = mblog.get('visible').get('list_id')
  data_w['time'] = formatTime(mblog.get('created_at'))

  # weibo['id'] = mblog.get('id')
  # weibo['idstr'] = mblog.get('idstr') # id, idstr and mid are the same
  weibo['mid'] = mblog.get('mid')
  weibo['mblogid'] = mblog.get('mblogid')
  weibo['uid'] = mblog.get('user').get('id')
  weibo['name'] = mblog.get('user').get('screen_name')

  data_w['profile_image_url'] = mblog.get('user').get('profile_image_url')
  data_w['profile_url'] = mblog.get('user').get('profile_url')
  data_w['verified'] = mblog.get('user').get('verified')
  data_w['verified_type'] = mblog.get('user').get('verified_type')
  data_w['domain'] = mblog.get('user').get('domain')
  data_w['weihao'] = mblog.get('user').get('weihao')
  data_w['verified_type_ext'] = mblog.get('user').get('verified_type_ext')
  data_w['avatar_large'] = mblog.get('user').get('avatar_large')
  data_w['avatar_hd'] = mblog.get('user').get('avatar_hd')
  data_w['follow_me'] = mblog.get('user').get('follow_me')
  data_w['following'] = mblog.get('user').get('following')
  data_w['mbrank'] = mblog.get('user').get('mbrank')
  data_w['mbtype'] = mblog.get('user').get('mbtype')
  data_w['planet_video'] = mblog.get('user').get('planet_video')
  data_w['planet_video'] = mblog.get('user').get('planet_video')
  data_w['icon_list'] = mblog.get('user').get('icon_list')

  data_w['can_edit'] = mblog.get('can_edit')
  data_w['textLength'] = mblog.get('textLength')
  data_w['source'] = mblog.get('source')
  data_w['favorited'] = mblog.get('favorited')
  data_w['cardid'] = mblog.get('cardid')
  data_w['cardid'] = mblog.get('cardid')
  data_w['pic_ids'] = mblog.get('pic_ids')
  data_w['geo'] = mblog.get('geo')
  data_w['pic_num'] = mblog.get('pic_num')
  data_w['is_paid'] = mblog.get('is_paid')
  data_w['mblog_vip_type'] = mblog.get('mblog_vip_type')
  # data_w['reposts_count'] = mblog.get('reposts_count')
  data_w['comments_count'] = mblog.get('comments_count')
  data_w['attitudes_count'] = mblog.get('attitudes_count')
  data_w['attitudes_status'] = mblog.get('attitudes_status')
  data_w['isLongText'] = mblog.get('isLongText')
  data_w['mlevel'] = mblog.get('mlevel')
  data_w['content_auth'] = mblog.get('content_auth')
  data_w['is_show_bulletin'] = mblog.get('is_show_bulletin')
  data_w['mblogtype'] = mblog.get('mblogtype')
  data_w['showFeedRepost'] = mblog.get('showFeedRepost')
  data_w['showFeedComment'] = mblog.get('showFeedComment')
  data_w['pictureViewerSign'] = mblog.get('pictureViewerSign')
  data_w['showPictureViewer'] = mblog.get('showPictureViewer')
  data_w['repost_type'] = mblog.get('repost_type')
  data_w['repost_type'] = mblog.get('repost_type')
  data_w['share_repost_type'] = mblog.get('share_repost_type')

  data_w['text'] = mblog.get('text_raw')
  if mblog.get('isLongText'):
    long_text = getLongText(mid, headers)
    if long_text is not None:
      data_w['text'] = removeHyperlinks(long_text)

  if mblog.get('reads_count'):
    data_w['reads_count'] = mblog.get('reads_count')
  
  tmpheaders = {
    "host": "weibo.com",
    "referer": 'https://weibo.com/u/' + str(uid),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
    "X-Requested-With": "XMLHttpRequest",
    "cookie": "SINAGLOBAL=3844073175642.917.1646038927204; UOR=cn.bing.com,weibo.com,cn.bing.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TJwnjDPbUTrv6-o6GTRi65JpX5KMhUgL.FoMESh5pehqpSKM2dJLoIpjLxK-L1K5LBoBLxK-LB-BLBKeLxKnL12BLBoMt; ULV=1648019064084:6:5:1:1626688394416.8887.1648019064073:1646318591445; ALF=1679563332; SSOLoginState=1648027333; SCF=Aky-rPXlPAOdGHx5MXGs4_kz0np45_lz7NkbNClQWg5AXrG7V021uZHdP9oLWozIexx_x0UsHlhdAKCp9lekzrY.; SUB=_2A25PPpaYDeRhGeFM71IQ8CjNzjuIHXVsTY9QrDV8PUNbmtAKLXikkW9NQMaAsGwx_HL3RGuup6TWf0MmFYKnOZsW; XSRF-TOKEN=BGBJHbLTh2-lFTLNp8D9eEcq; WBPSESS=Yd3BHei0Ouk_WjPV5pHB2jcZdi1sNpW6Fv385DTeZor-JBFuOmvuOf0bYOmfJfuCGUqCXlyhNDqqfipi4m2gPmBe4nRE39OsBFuG4aQkkV_-tlQPi5sME-dCBXAWem4slHWQX9YpaoXz_yHXrKxHZA=="
  }
  
  userInfo = getUserInfo(uid, tmpheaders)
  print('userInfo', userInfo)
  if userInfo is not None:
    data_w['userInfo'] = userInfo
  
  userDetail = getUserDetail(uid, tmpheaders)
  if userDetail is not None:
    data_w['userDetail'] = userDetail
  
  weibo['data'] = data_w

  return weibo


# select a initial page https://weibo.com/2656274875/LdOT4awvY 
# on the page https://weibo.com/2656274875/LdOT4awvY type F12 to view the responses of the link "https://weibo.com/ajax/statuses/show?id="
def getWeibo(mid, uid, headers):
  url = "https://weibo.com/ajax/statuses/show?id=" + mid
  try:
    response = requests.get(url = url, headers = headers)
    if response.status_code == 200:
      mblog = response.json()
      weibo = reponseInfo2Dict(mid, uid, mblog)
      return weibo
    else:
      print(response.status_code, response.content, flush = True)
  except Exception as e:
    print('Error', e, flush = True)

  return None

# get the page with comments
# on the page https://weibo.com/2656274875/LdOT4awvY#repost type F12 to view the responses
def get_page(params, headers):
  url = "https://weibo.com/ajax/statuses/repostTimeline?" + urlencode(params)
  try:
    response = requests.get(url = url, headers = headers, timeout = 10)
    if response.status_code == 200:
      data = response.json()
      return data
    else:
      print(response.status_code, response.content, flush = True)
  except Exception as e:
    print('Error', e, flush = True)

  return None

def parse_data(data, pid):
  if data is None:
    return None, []
  max_page = data.get('max_page')
  lists = data.get('data')
  weibos = []
  for mblog in lists:
    if mblog:
      mid = mblog.get('mid')
      uid = mblog.get('user').get('id')
      weibo = reponseInfo2Dict(mid, uid, mblog)
      weibo['pid'] = pid # parent id

      # if 'retweeted_status' in mblog:
      #   weibo['pid'] = mblog.get('retweeted_status').get('mid') 这里的mid保存的还是原始根的id

      # if weibo['reposts_count'] > 0 and not (weibo['mid'] in seeds_set):
      if not (weibo['mid'] in seeds_set):
        # 原始注释：不用爬子微博的转发，全部微博的转发，包括子微博
        # 当前注释：需要爬取微博转发，因为需要标记父子节点
        seeds_set.add(weibo['mid'])
        seeds.put([weibo['uid'], weibo['mid']])

      weibos.append(weibo)

  return max_page, weibos


def get_repost(uid, mid):
  global all_weibos
  global headers
  global new_weibo_zero_count
  max_page = -1
  print('https://weibo.com/' + str(uid) + '/' + mid_to_url(mid), flush = True)
  i = 1
  try:
    while True:
      if max_page is None or  (max_page > 0 and i > max_page):
        break
      params = {
        'id': mid,
        'page': i,
        'moduleID': 'feed'
      }
      return_max_page, new_weibos = parse_data(get_page(params, headers), mid)
      if max_page < 0 and return_max_page > 0:
        max_page = return_max_page

      time.sleep(random.randint(1, 20) / 10)

      all_weibos = all_weibos + new_weibos
      
      print('page ', i, 'weibos', len(new_weibos), flush = True)
      
      if len(new_weibos) == 0:
        new_weibo_zero_count += 1
      # else:
      #   new_weibo_zero_count = 0

      if new_weibo_zero_count > 20:
        break
      
      print('all_weibos', len(all_weibos), flush = True)
      i = i + 1

      if i > 200:
        break
  
  except Exception as e:
    print(e)

def timeSort(ele):
  return ele['data']['time']

outputFolder = 'repost/'
if not os.path.exists(outputFolder):
  os.mkdir(outputFolder)

saveFilePath = './hotlinks/link.csv'
# get_repost_1(limit_pages=10,filepath=saveFilePath)
df = pd.read_csv(saveFilePath)
weibo_links = df['hotlink'].values.tolist()


for weibo_link in weibo_links:
  weibo_url = weibo_link.split('/')[-1]
  weibo_mid = url_to_mid(weibo_url)
  weibo_uid = int(weibo_link.split('/')[-2])

  headers = {
    "host": "weibo.com",
    "referer": 'https://weibo.com/' + str(weibo_uid) + '/' + weibo_url,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
    "X-Requested-With": "XMLHttpRequest",
    "cookie": "SINAGLOBAL=7987140213946.333.1605197641875; ULV=1634042457745:13:1:1:9576227501281.14.1634042457599:1629965688140; UOR=www.baidu.com,open.weibo.com,graph.qq.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52RrXUDmguX9ziQ3WqVIvK5JpX5KMhUgL.Foz0So.p1Kq0eo22dJLoIERLxKqL1h.L12zLxKqL1-eLB.2LxKML1KBLBKnLxKqL1hnLBoMEe0q4eK.ce0zp; ALF=1670984896; SSOLoginState=1639448897; SCF=At0UCYTaVqZdpgptq7SljVF9oPcWVnVo1vpzYbKpbsYdUhWfJo4ebQkmKG13djiO1EvkNNlBxc28AOu3NyNla7Q.; SUB=_2A25MvHESDeRhGeRN7VsQ-SjPyT2IHXVvyOXarDV8PUNbmtAKLVjWkW9NU5xMaaFQMY6v_Ea76IKUbqFDW63CQcuF; XSRF-TOKEN=PmuMolp20oh352q43nj9LcJX; WBPSESS=oaqfGpuBr7-UtSFsCHFHSt5RxL-hYYU20puv2cqW1qVBK96zsIx7SS3-E5l8Mt_rOXUxi71lSsdyfYHpgM98bw3_gJkws4d95T9eniXCEHgn6ZFOmXqgr_8MNFTEl2ZvTqfac5MrTHtBjPjeTYGtEA=="
  }

  all_weibos = []
  all_weibos.append(getWeibo(weibo_mid, weibo_uid, headers))
  new_weibo_zero_count = 0

  seeds = Queue()
  seeds.put([weibo_uid, weibo_mid])

  seeds_set = set()
  while not seeds.empty():
    a = seeds.get()
    print(a)
    get_repost(a[0], a[1])

  final_weibos = clean(all_weibos)
  final_weibos.sort(key = timeSort)
  print('final_weibos', len(final_weibos), flush = True)

  outputFileName = outputFolder + '/' + weibo_url + str(len(final_weibos)) + '.json'
  outputFile = open(outputFileName, "w", encoding='utf-8')
  json.dump(final_weibos, outputFile, ensure_ascii=False)
  outputFile.close()
  print("==============================")
