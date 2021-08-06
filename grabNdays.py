# %%
import datetime
import time
import pandas as pd
from io import StringIO
from function_grab import grab_price
import numpy as np
import warnings
import random

data = {}
n_days = 120
date = datetime.datetime.now()
fail_count = 0
allow_continuous_fail_count = 15  # 近五年最長連續12天休市
while len(data) < n_days:

    print('parsing', date)
    # 使用 grabPrice 爬資料
    try:
        # 抓資料
        data[date.date()] = grab_price(date)
        print('success!')
        fail_count = 0
    except:
        # 假日爬不到
        print('fail! check the date is holiday')
        fail_count += 1
        if fail_count == allow_continuous_fail_count:
            raise
            break

    # 減一天
    date -= datetime.timedelta(days=1)
    time.sleep(random.randint(5, 10))
updown = pd.DataFrame({k: d['漲跌(+/-)'] for k, d in data.items()})
# print(updown)
# %%
trade_n = pd.DataFrame({k: d['成交股數'] for k, d in data.items()})
i = 0
while i <= trade_n.shape[0]-1:
    trade_n.iloc[i] = trade_n.iloc[i].str.replace(',', '')
    trade_n.iloc[i] = round(trade_n.iloc[i].astype(float)/1000)
    i += 1
# print(trade_n)

PEratio = pd.DataFrame({k: d['本益比'] for k, d in data.items()})
i = 0
while i <= PEratio.shape[0]-1:
    PEratio.iloc[i] = PEratio.iloc[i].str.replace(',', '')
    i += 1

updown.to_excel('grab120days_updown.xlsx')
trade_n.to_excel('grab120days_traden.xlsx')
PEratio.to_excel('grab120days_PE.xlsx')
# print(trade_n)
# print(PEratio)
close = pd.DataFrame({k: d['收盤價'] for k, d in data.items()})  # type=string
# print(close)
# print(close.shape)
# %%
# MA5
i = 0
MA5 = []
close = close.replace('--', np.NaN)
while i <= close.shape[0]-1:
    close.iloc[i] = close.iloc[i].str.replace(',', '')
    mean = np.nanmean(close.iloc[i, 0:5].astype(float))
    # print(mean)
    MA5.append([close.index[i], mean])
    i = i+1
# 先創造空list使計算值與代號存入，而後將list存入df中，將一列設為index，使用merge針對匹配的index進行合併，空值存入NaN
MA5 = pd.DataFrame(MA5, columns=['證券代號', 'MA5']).set_index('證券代號')
close = pd.merge(close, MA5, how='outer', left_index=True, right_index=True)
# 必須將dtype轉為float(與算出來的平均值同樣型態)，否則在後面merge的時候會因為型別不一樣而存成NaN
close = close.astype(float)  # 全轉float

# MA20
i = 0
MA20 = []
# print(close.shape) #df.shape=(n_rows,n_columns)
# 將有收盤價的資料存入np.nan 在後面使用np.mean時可以直接跳過不加入平均值的計算
# close = close.replace('--', np.NaN)   replace只能針對字符串全等於才能替換
while i <= close.shape[0]-1:
    # dataframe中需使用iloc對索引編號定位，loc是針對索引名稱進行定位
    # print(type(close.iloc[i, 1]))
    # 針對某一列的字符串進行replace才能將千分位符號消去
    # close.iloc[i] = close.iloc[i].str.replace(',', '')
    # print(close.iloc[i, 0:3])
    # astype只是將資料暫時當作別的型態使用，而不是真的更改 除非有另外存回變數
    mean = np.nanmean(close.iloc[i, 0:20])
    # print(type(close.iloc[i, 1]))

    """for j in range(3):
        close.iloc[i, j] = close.iloc[i, j].replace(',', '')
        sum = sum + float(close.iloc[i, j])
        print(sum)
    mean = sum/3"""

    # print(mean)
    MA20.append([close.index[i], mean])
    i = i+1
# 先創造空list使計算值與代號存入，而後將list存入df中，將一列設為index，使用merge針對匹配的index進行合併，空值存入NaN
MA20 = pd.DataFrame(MA20, columns=['證券代號', 'MA20']).set_index('證券代號')
close = pd.merge(close, MA20, how='outer', left_index=True, right_index=True)
print(close)
close = close.astype(float)

# MA60
i = 0
MA60 = []
while i <= close.shape[0]-1:
    mean = np.nanmean(close.iloc[i, 0:60])
    MA60.append([close.index[i], mean])
    i = i+1
MA60 = pd.DataFrame(MA60, columns=['證券代號', 'MA60']).set_index('證券代號')
close = pd.merge(close, MA60, how='outer', left_index=True, right_index=True)
print(close)
close = close.astype(float)
# %%
# MA120
i = 0
MA120 = []
while i <= close.shape[0]-1:
    mean = np.nanmean(close.iloc[i, 0:120])
    MA120.append([close.index[i], mean])
    i = i+1
MA120 = pd.DataFrame(MA120, columns=['證券代號', 'MA120']).set_index('證券代號')
close = pd.merge(close, MA120, how='outer', left_index=True, right_index=True)
print(close)
close = close.astype(float)

# print(close)
close.to_excel('stock120.xlsx')
