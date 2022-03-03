#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:wjher

# https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=102803&containerid=102803&extparam=discover%7Cnew_feed&max_id=3&count=10
# https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=102803&containerid=102803&extparam=discover%7Cnew_feed&max_id=2&count=10
# https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=0&group_id=102803&containerid=102803&extparam=discover%7Cnew_feed&max_id=0&count=10

import requests
from urllib.parse import urlencode
import random
import time
import numpy as np
import pandas as pd
import os

def get_page_1(params, headers):
  url = "https://weibo.com/ajax/feed/hottimeline?" + urlencode(params)
  try:
    response = requests.get(url=url, headers=headers, timeout=10)
    if response.status_code == 200:
      data = response.json()
      return data
    else:
      print(response.status_code, response.content, flush=True)
  except Exception as e:
    print('Error', e, flush=True)
  return None

# 解析页面
def parse_data_1(data,filepath:str):
  if data is None:
    return None, []

  lists = data.get('statuses')
  weibos = []
  for mblog in lists:
    if mblog:
      weibo = {}
      weibo['mid'] = mblog.get('mid')
      weibo['mblogid'] = mblog.get('mblogid')
      weibo['uid'] = str(mblog.get('user').get('id'))
      weibo['name'] = mblog.get('user').get('screen_name')
      link = {}
      link['hotlink'] = 'https://weibo.com/' + weibo['uid'] + '/' + weibo['mblogid']
      save_csv(filepath, link, Label=False if os.path.exists(filepath) else True)
      weibos.append(weibo)
  return weibos

def save_csv(path:str, content:dict, Label:bool):
    df = pd.DataFrame(np.array([list(content.values())]),columns=list(content.keys()))
    df.to_csv(path, index=False, mode='a', header=Label)

def get_repost_1(limit_pages:int,filepath:str):
  global headers
  i = 0
  try:
    while True:
      params = {
        'refresh': 2,
        'group_id': 102803,
      	'containerid': 102803,
      	'extparam': 'discover|new_feed',
      	'max_id': i,
      	'count': 10
      }
      new_weibos = parse_data_1(get_page_1(params, headers),filepath)
      time.sleep(random.randint(1, 20) / 10)
      print(new_weibos)
      i = i + 1
      if i > limit_pages:
        break
  except Exception as e:
    print(e)


headers = {
    "host": "weibo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62",
    "X-Requested-With": "XMLHttpRequest",
    # "Connection": "keep-alive",
    # "cookie": "SINAGLOBAL=3844073175642.917.1646038927204; ULV=1646038927210:1:1:1:3844073175642.917.1646038927204:; ALF=1677575089; SSOLoginState=1646039089; SUB=_2A25PGOBhDeRhGeFM71IQ8CjNzjuIHXVsbFaprDV8PUNbmtAKLRLQkW9NQMaAsEQm7Z-THVd8lEvJAVF1L8TfsStE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TJwnjDPbUTrv6-o6GTRi65JpX5KzhUgL.FoMESh5pehqpSKM2dJLoIpjLxK-L1K5LBoBLxK-LB-BLBKeLxKnL12BLBoMt; XSRF-TOKEN=SQlqZOqYROWj9jQ46UcFm_S_; WBPSESS=Yd3BHei0Ouk_WjPV5pHB2jcZdi1sNpW6Fv385DTeZor-JBFuOmvuOf0bYOmfJfuC_oiNE0xuuBJVkOgbf7MaqDR7Qz9buefW7SSfh2CDXHKvJb5DnczIxg6YQLd8J0S6opt-2cBdbO29PFSWyXN-oQ=="
    "cookie": "SINAGLOBAL=7987140213946.333.1605197641875; ULV=1634042457745:13:1:1:9576227501281.14.1634042457599:1629965688140; UOR=www.baidu.com,open.weibo.com,graph.qq.com; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W52RrXUDmguX9ziQ3WqVIvK5JpX5KMhUgL.Foz0So.p1Kq0eo22dJLoIERLxKqL1h.L12zLxKqL1-eLB.2LxKML1KBLBKnLxKqL1hnLBoMEe0q4eK.ce0zp; ALF=1670984896; SSOLoginState=1639448897; SCF=At0UCYTaVqZdpgptq7SljVF9oPcWVnVo1vpzYbKpbsYdUhWfJo4ebQkmKG13djiO1EvkNNlBxc28AOu3NyNla7Q.; SUB=_2A25MvHESDeRhGeRN7VsQ-SjPyT2IHXVvyOXarDV8PUNbmtAKLVjWkW9NU5xMaaFQMY6v_Ea76IKUbqFDW63CQcuF; XSRF-TOKEN=PmuMolp20oh352q43nj9LcJX; WBPSESS=oaqfGpuBr7-UtSFsCHFHSt5RxL-hYYU20puv2cqW1qVBK96zsIx7SS3-E5l8Mt_rOXUxi71lSsdyfYHpgM98bw3_gJkws4d95T9eniXCEHgn6ZFOmXqgr_8MNFTEl2ZvTqfac5MrTHtBjPjeTYGtEA=="
}

# get_repost_1(limit_pages=10,filepath='./hotlinks/link1.csv')