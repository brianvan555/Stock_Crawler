# %%
import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime

date = datetime.datetime.now()

# 下載股價
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' +
                  str(date).split(' ')[0].replace('-', '') + '&type=ALL')
# 包含所有指標、期貨等等
'''df = pd.read_csv(StringIO(r.text.replace("=", "")),
                 header=["證券代號" in l for l in r.text.split("\n")].index(True)-1)'''
# 僅包含股票
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                     for i in r.text.split('\n')
                                     if len(i.split('",')) == 17 and i[0] != '='])), header=0)
df = df.set_index("證券代號")
# %% 交易股數
stk_name = pd.DataFrame(df['證券名稱'])
print(stk_name)
stk_name.to_excel('stock_name.xlsx')
# %% create user dict
path = 'user_dict.txt'
with open(path, 'w', encoding='utf-8') as f:
    i = 0
    while i < stk_name.shape[0]-1:
        f.write(stk_name.iloc[i, 0]+'\n')
        i += 1
