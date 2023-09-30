# Stock_Crawler
It's a TWSE crawlers which can freely add any conditions to filter, and perform data visualization by word cloud. 

## Enviroment
- Python 3.9
- wordcloud 1.8.1
- jieba 0.42.1

## How to use
1. Run grabNdays.py to get data from TWSE (first time)
2. Run insertNewday.py to add new data join to current table
3. Update all stock name & number by stk_name.py
4. Run word_cloud.py to generate wordcloud image base on your conditions
   
## Demo
Word Cloud<br>
![Word Cloud](img/Demo.png)