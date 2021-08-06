# %%
import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import time
import warnings
import random

date = datetime.datetime.now()

# 下載股價
r = requests.post('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' +
                  str(date).split(' ')[0].replace('-', '') + '&type=ALL')
# 僅包含股票
df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '})
                                     for i in r.text.split('\n')
                                     if len(i.split('",')) == 17 and i[0] != '='])), header=0)
df = df.set_index("證券代號")
# %% 交易股數
trade_n = pd.DataFrame(df['成交股數'])
trade_n.rename(columns={trade_n.columns[0]: date.date()}, inplace=True)
i = 0
while i <= trade_n.shape[0]-1:
    trade_n.iloc[i] = trade_n.iloc[i].str.replace(',', '')
    trade_n.iloc[i] = round(trade_n.iloc[i].astype(float)/1000)
    i += 1
trades = pd.read_excel('traden_acc.xlsx')
trades = pd.merge(trade_n, trades, on='證券代號')
trades = trades.set_index("證券代號")
trades.to_excel('traden_acc.xlsx')

# %% 本益比
PEratio = pd.DataFrame(df['本益比'])
PEratio.rename(columns={PEratio.columns[0]: date.date()}, inplace=True)
i = 0
while i <= PEratio.shape[0]-1:
    PEratio.iloc[i] = PEratio.iloc[i].str.replace(',', '')
    i += 1
PEratios = pd.read_excel('PEratio_acc.xlsx')
PEratios = pd.merge(PEratio, PEratios, on='證券代號')
PEratios = PEratios.set_index("證券代號")
PEratios.to_excel('PEratio_acc.xlsx')

# %% 漲跌幅
updown = pd.DataFrame(df['漲跌(+/-)'])
updown.rename(columns={updown.columns[0]: date.date()}, inplace=True)
updowns = pd.read_excel('updown_acc.xlsx')
updowns = pd.merge(updown, updowns, on='證券代號')
updowns = updowns.set_index("證券代號")
updowns.to_excel('updown_acc.xlsx', na_rep='NaN')

# %% 收盤價
close = pd.DataFrame(df['收盤價'])
close.rename(columns={close.columns[0]: date.date()}, inplace=True)
i = 0
while i <= close.shape[0]-1:
    close.iloc[i] = close.iloc[i].str.replace(',', '')
    i += 1
closes = pd.read_excel('closes_acc.xlsx')
closes = pd.merge(closes, closes, on='證券代號')
closes = closes.set_index("證券代號")
# 重新計算MA
# MA5
i = 0
MA5 = []
closes = closes.replace('--', np.NaN)
while i <= closes.shape[0]-1:
    print(i)
    mean = np.nanmean(closes.iloc[i, 0:5].astype(float))
    # print(mean)
    MA5.append([closes.index[i], mean])
    i = i+1

MA5 = pd.DataFrame(MA5, columns=['證券代號', 'MA5']).set_index('證券代號')
closes = pd.merge(closes, MA5, how='outer', left_index=True, right_index=True)
closes = closes.astype(float)

# MA20
i = 0
MA20 = []
while i <= closes.shape[0]-1:
    print(i)
    mean = np.nanmean(closes.iloc[i, 0:20])
    MA20.append([closes.index[i], mean])
    i = i+1

MA20 = pd.DataFrame(MA20, columns=['證券代號', 'MA20']).set_index('證券代號')
closes = pd.merge(closes, MA20, how='outer', left_index=True, right_index=True)
print(closes)
closes = closes.astype(float)

# MA60
i = 0
MA60 = []
while i <= closes.shape[0]-1:
    print(i)
    mean = np.nanmean(closes.iloc[i, 0:60])
    MA60.append([closes.index[i], mean])
    i = i+1
MA60 = pd.DataFrame(MA60, columns=['證券代號', 'MA60']).set_index('證券代號')
closes = pd.merge(closes, MA60, how='outer', left_index=True, right_index=True)
print(closes)
closes = closes.astype(float)

# MA120
i = 0
MA120 = []
while i <= closes.shape[0]-1:
    print(i)
    mean = np.nanmean(closes.iloc[i, 0:120])
    MA120.append([closes.index[i], mean])
    i = i+1
MA120 = pd.DataFrame(MA120, columns=['證券代號', 'MA120']).set_index('證券代號')
closes = pd.merge(closes, MA120, how='outer',
                  left_index=True, right_index=True)
print(closes)
closes = closes.astype(float)

closes.to_excel('closes_acc.xlsx')
