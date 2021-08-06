import requests
from io import StringIO
import pandas as pd
import numpy as np
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.3.4382342.1624324217; _ga_F4L5BYPQDJ=GS1.1.1627522340.1.1.1627522368.0; _gid=GA1.3.2021134005.1627800072; JSESSIONID=7EB287947AAEDBB78D3F2CF861E2E493",
    "Host": "www.twse.com.tw",
    "Referer": "https://www.twse.com.tw/zh/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}


def grab_price(date):
    r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' +
                      str(date).split(' ')[0].replace('-', '') + '&type=ALL', headers=headers)

    ret = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                          for i in r.text.split('\n')
                                          if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    ret = ret.set_index('證券代號')
    # ret['成交金額'] = ret['成交金額'].str.replace(',', '') 無效
    #ret['成交股數'] = ret['成交股數'].str.replace(',', '')
    return ret
