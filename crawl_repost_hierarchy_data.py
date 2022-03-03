#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Fixed by:wjher
# reference: https://blog.csdn.net/HandsomeFishman

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
    # >>> mid_to_url(3501703397689247)
    # 'z0Ijpwgk7'
    # >>> mid_to_url(3501701648871479)
    # 'z0IgABdSn'
    # >>> mid_to_url(3500330408906190)
    # 'z08AUBmUe'
    # >>> mid_to_url(3500247231472384)
    # 'z06qL6b28'
    
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
    # >> url_to_mid('z0Ijpwgk7')
    # 3501703397689247L
    # >> url_to_mid('z0IgABdSn')
    # 3501701648871479L
    # >> url_to_mid('z08AUBmUe')
    # 3500330408906190L
    # >> url_to_mid('z06qL6b28')
    # 3500247231472384L

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
  # c 先在a里面加入了，然后又在b里面加入了
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
    print('错误', e.args, flush = True)
  return None

def reponseInfo2Dict(mid, mblog):
  weibo = {}
  weibo['visible_type'] = mblog.get('visible').get('type')
  weibo['visible_list_id'] = mblog.get('visible').get('list_id')
  weibo['time'] = formatTime(mblog.get('created_at'))
  # weibo['id'] = mblog.get('id')
  # weibo['idstr'] = mblog.get('idstr') # id idstr 两者与mid相同
  weibo['mid'] = mblog.get('mid')
  weibo['mblogid'] = mblog.get('mblogid')

  weibo['uid'] = mblog.get('user').get('id')
  weibo['name'] = mblog.get('user').get('screen_name')
  weibo['profile_image_url'] = mblog.get('user').get('profile_image_url')
  weibo['profile_url'] = mblog.get('user').get('profile_url')
  weibo['verified'] = mblog.get('user').get('verified')
  weibo['verified_type'] = mblog.get('user').get('verified_type')
  weibo['domain'] = mblog.get('user').get('domain')
  weibo['weihao'] = mblog.get('user').get('weihao')
  weibo['verified_type_ext'] = mblog.get('user').get('verified_type_ext')
  weibo['avatar_large'] = mblog.get('user').get('avatar_large')
  weibo['avatar_hd'] = mblog.get('user').get('avatar_hd')
  weibo['follow_me'] = mblog.get('user').get('follow_me')
  weibo['following'] = mblog.get('user').get('following')
  weibo['mbrank'] = mblog.get('user').get('mbrank')
  weibo['mbtype'] = mblog.get('user').get('mbtype')
  weibo['planet_video'] = mblog.get('user').get('planet_video')
  weibo['planet_video'] = mblog.get('user').get('planet_video')
  weibo['icon_list'] = mblog.get('user').get('icon_list')

  weibo['can_edit'] = mblog.get('can_edit')
  weibo['textLength'] = mblog.get('textLength')
  weibo['source'] = mblog.get('source')
  weibo['favorited'] = mblog.get('favorited')
  weibo['cardid'] = mblog.get('cardid')
  weibo['cardid'] = mblog.get('cardid')
  weibo['pic_ids'] = mblog.get('pic_ids')
  weibo['geo'] = mblog.get('geo')
  weibo['pic_num'] = mblog.get('pic_num')
  weibo['is_paid'] = mblog.get('is_paid')
  weibo['mblog_vip_type'] = mblog.get('mblog_vip_type')
  weibo['reposts_count'] = mblog.get('reposts_count')
  weibo['comments_count'] = mblog.get('comments_count')
  weibo['attitudes_count'] = mblog.get('attitudes_count')
  weibo['attitudes_status'] = mblog.get('attitudes_status')
  weibo['isLongText'] = mblog.get('isLongText')
  weibo['mlevel'] = mblog.get('mlevel')
  weibo['content_auth'] = mblog.get('content_auth')
  weibo['is_show_bulletin'] = mblog.get('is_show_bulletin')
  weibo['mblogtype'] = mblog.get('mblogtype')
  weibo['showFeedRepost'] = mblog.get('showFeedRepost')
  weibo['showFeedComment'] = mblog.get('showFeedComment')
  weibo['pictureViewerSign'] = mblog.get('pictureViewerSign')
  weibo['showPictureViewer'] = mblog.get('showPictureViewer')
  weibo['repost_type'] = mblog.get('repost_type')
  weibo['repost_type'] = mblog.get('repost_type')
  weibo['share_repost_type'] = mblog.get('share_repost_type')

  weibo['text'] = mblog.get('text_raw')
  if mblog.get('isLongText'):
    long_text = getLongText(mid, headers)
    if long_text is not None:
      weibo['text'] = removeHyperlinks(long_text)

  if mblog.get('reads_count'):
    weibo['reads_count'] = mblog.get('reads_count')

  return weibo


# 获取样例，比如 https://weibo.com/2656274875/LdOT4awvY 的状态信息，可以称之为初始起点
# 在页面 https://weibo.com/2656274875/LdOT4awvY 下F12可查看
def getWeibo(mid, headers):
  url = "https://weibo.com/ajax/statuses/show?id=" + mid
  try:
    response = requests.get(url = url, headers = headers)
    if response.status_code == 200:
      mblog = response.json()
      weibo = reponseInfo2Dict(mid, mblog)
      return weibo
    else:
      print(response.status_code, response.content, flush = True)
  except Exception as e:
    print('错误', e, flush = True)

  return None

# 返回带有评论的页面
# 在页面 https://weibo.com/2656274875/LdOT4awvY#repost 下F12可查看
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
    print('错误', e, flush = True)

  return None


# 解析页面
def parse_data(data, pid):
  if data is None:
    return None, []
  max_page = data.get('max_page')
  lists = data.get('data')
  weibos = []
  for mblog in lists:
    if mblog:
      mid = mblog.get('mid')
      weibo = reponseInfo2Dict(mid, mblog)
      # pid to find the node's parent node
      weibo['pid'] = pid

      # if 'retweeted_status' in mblog:
      #   weibo['pid'] = mblog.get('retweeted_status').get('mid') 这里的mid保存的还是原始根的id

      if weibo['reposts_count'] > 0 and not (weibo['mid'] in seeds_set):
        # print(weibo['text'])
        # 每个非空的种子进去，导致重复爬取。。。。，
        # 
        # 原始注释：不用爬子微博的转发，全部微博的转发，包括子微博
        # 当前注释：需要爬取微博转发，因为需要标记父子节点
        seeds_set.add(weibo['mid'])
        seeds.put([weibo['uid'], weibo['mid']])

      weibos.append(weibo)

  return max_page, weibos


def get_repost(uid, mid):
  global all_weibos
  global headers
  max_page = -1
  print('https://weibo.com/' + uid + '/' + mid_to_url(mid), flush = True)
  i = 1
  new_weibo_zero_count = 0
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
      else:
        new_weibo_zero_count = 0

      if new_weibo_zero_count > 20:
        break
      
      print('all_weibos', len(all_weibos), flush = True)
      i = i + 1
  
  except Exception as e:
    print(e)

def timeSort(ele):
  return ele['time']

outputFolder = 'repost/'
if not os.path.exists(outputFolder):
  os.mkdir(outputFolder)



# 先获取热点链接
saveFilePath = './hotlinks/link.csv'
# get_repost_1(limit_pages=10,filepath=saveFilePath)
# 读取热点链接
df = pd.read_csv(saveFilePath)
weibo_links = df['hotlink'].values.tolist()

for weibo_link in weibo_links:
  weibo_url = weibo_link.split('/')[-1]
  # print(type(weibo_url))
  weibo_mid = url_to_mid(weibo_url)
  weibo_uid = weibo_link.split('/')[-2]
  headers = {
    "host": "weibo.com",
    "referer": 'https://weibo.com/' + weibo_uid + '/' + weibo_url,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
    "X-Requested-With": "XMLHttpRequest",
    # "Connection": "keep-alive",
    # "cookie": "SINAGLOBAL=7734682608780.217.1646061411766; SSOLoginState=1646114748; SUB=_2A25PGcfsDeRhGeFM71IQ8CjNzjuIHXVs5emkrDV8PUJbkNAKLWLdkW1NQMaAsDNb1Vx7Aknn0dOcx3Q4YFNSIwYo; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TJwnjDPbUTrv6-o6GTRi65NHD95QNeoB7eK5ceK-NWs4Dqcjdi--fiK.7i-zXi--fi-82i-20i--RiKy2i-zN; XSRF-TOKEN=cKFBbFnkLbBdI9yqmP2IcMEr; _s_tentry=weibo.com; Apache=8764286467942.853.1646126060538; ULV=1646126060566:2:1:2:8764286467942.853.1646126060538:1646061411774; trdipcktrffcext=1; WBPSESS=Yd3BHei0Ouk_WjPV5pHB2jcZdi1sNpW6Fv385DTeZor-JBFuOmvuOf0bYOmfJfuCylgA_dPMdE7DuKZXuhtpy7SEv900AXWYggrXLrCAK6Gq1Cda1A1sIpPf1tb9MctmWdskh336eXxP-_KEQFmGPg=="
    # "cookie": "SINAGLOBAL=3844073175642.917.1646038927204; ULV=1646038927210:1:1:1:3844073175642.917.1646038927204:; ALF=1677575089; SSOLoginState=1646039089; SUB=_2A25PGOBhDeRhGeFM71IQ8CjNzjuIHXVsbFaprDV8PUNbmtAKLRLQkW9NQMaAsEQm7Z-THVd8lEvJAVF1L8TfsStE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TJwnjDPbUTrv6-o6GTRi65JpX5KzhUgL.FoMESh5pehqpSKM2dJLoIpjLxK-L1K5LBoBLxK-LB-BLBKeLxKnL12BLBoMt; XSRF-TOKEN=SQlqZOqYROWj9jQ46UcFm_S_; WBPSESS=Yd3BHei0Ouk_WjPV5pHB2jcZdi1sNpW6Fv385DTeZor-JBFuOmvuOf0bYOmfJfuC_oiNE0xuuBJVkOgbf7MaqDR7Qz9buefW7SSfh2CDXHKvJb5DnczIxg6YQLd8J0S6opt-2cBdbO29PFSWyXN-oQ=="
    "cookie": "SINAGLOBAL=7987140213946.333.1605197641875; ULV=1634042457745:13:1:1:9576227501281.14.1634042457599:1629965688140; UOR=www.baidu.com,open.weibo.com,graph.qq.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52RrXUDmguX9ziQ3WqVIvK5JpX5KMhUgL.Foz0So.p1Kq0eo22dJLoIERLxKqL1h.L12zLxKqL1-eLB.2LxKML1KBLBKnLxKqL1hnLBoMEe0q4eK.ce0zp; ALF=1670984896; SSOLoginState=1639448897; SCF=At0UCYTaVqZdpgptq7SljVF9oPcWVnVo1vpzYbKpbsYdUhWfJo4ebQkmKG13djiO1EvkNNlBxc28AOu3NyNla7Q.; SUB=_2A25MvHESDeRhGeRN7VsQ-SjPyT2IHXVvyOXarDV8PUNbmtAKLVjWkW9NU5xMaaFQMY6v_Ea76IKUbqFDW63CQcuF; XSRF-TOKEN=PmuMolp20oh352q43nj9LcJX; WBPSESS=oaqfGpuBr7-UtSFsCHFHSt5RxL-hYYU20puv2cqW1qVBK96zsIx7SS3-E5l8Mt_rOXUxi71lSsdyfYHpgM98bw3_gJkws4d95T9eniXCEHgn6ZFOmXqgr_8MNFTEl2ZvTqfac5MrTHtBjPjeTYGtEA=="
  }

  all_weibos = []
  all_weibos.append(getWeibo(weibo_mid, headers))

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
