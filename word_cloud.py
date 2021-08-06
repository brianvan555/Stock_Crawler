from PIL import Image
from jieba.analyse import extract_tags
from os import path
import pandas as pd
import wordcloud as wc
import jieba


# 短線多頭
df = pd.read_excel('closes_acc.xlsx', index_col=0)  # 讀excel放入物件中
buyin = (df.iloc[:, 0] > df.iloc[:, -4]
         ) & (df.iloc[:, -4] > df.iloc[:, -3])  # 編寫條件
df = pd.DataFrame(df.index[buyin])  # 找出符合條件的index並轉成df存入
print(df)
# %%
# 合併成交量
df1 = pd.read_excel('traden_acc.xlsx', index_col=0)
df1.rename(columns={df1.columns[0]: "traden"},
           inplace=True)  # 修改col名稱方便後續排序時的呼叫
trade50 = (df1.iloc[:, 0].astype(float) > 40000) & (df1.iloc[:, 1].astype(float) > 40000) & (
    df1.iloc[:, 0:2].astype(float).sum(axis=1) > 130000)  # 延row進行總和計算 axis=1 前兩個交易日分別大於5W總和大於13W
df1 = df1[trade50].iloc[:, 0]  # 找出符合條件的存入df1
print(df1)
df2 = pd.merge(df, df1, on='證券代號')  # 合併df 由交集的方式
df2 = df2.sort_values(by=['traden'], ascending=False)  # 倒序排列成交量
print(df2)
# %% 加入名稱
df3 = pd.read_excel('stock_name.xlsx', index_col=0)
df3 = pd.merge(df2, df3, on='證券代號')
df3 = df3.set_index('證券代號')
print(df3)
print(df3.iloc[0, 1])
# %% wordlcoud
path = 'test.txt'
with open(path, 'w', encoding='utf-8') as f:
    i = 0
    while i < df3.shape[0]:
        for j in range(int(df3.iloc[i, 0]/1000)):
            f.write(df3.iloc[i, 1])
        i += 1
        '''for i in range(int(df3.iloc[0, 0]/1000)):
            f.write(df3.iloc[0, 1])
        for j in range(int(df3.iloc[1, 0]/1000)):
            f.write(df3.iloc[1, 1])'''
# %% jieba NLP chinese
text = open('test.txt', 'r', encoding='utf-8').read()
jieba.load_userdict('user_dict.txt')
text = ' '.join(jieba.cut(text))
tags = extract_tags(text, topK=5, withWeight=True)
for tag in tags:
    print('word:', tag[0], 'tf-idf:', tag[1])
# mask img
'''mask_color = np.array(Image.open('parrot.jpg'))
mask_color = mask_color[::3, ::3]
mask_image = mask_color.copy()
mask_image[mask_image.sum(axis=2) == 0] = 255'''
cloud = wc.WordCloud(font_path='TWSung.otf',
                     collocations=False, background_color='white').generate(text)
cloud.to_file('test.png')
# show img
im = Image.open('test.png')
im.show()
