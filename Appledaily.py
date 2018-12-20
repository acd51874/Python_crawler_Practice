import requests
import os
import ssl
from bs4 import BeautifulSoup
import jieba

# for MacOS
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

articleTextList = []
articleUrlList = []
contentAll = [] # the list of every article
wordEachArticle = [] # consider one single article, each element in the list is the set of words in that article
# that is , wordEachArticle[1] will be a list [word1, word2, .....]
wordCounter = {}

res = requests.get('https://tw.news.appledaily.com/headline/daily', headers = headers)

soup = BeautifulSoup(res.text, 'html.parser')
allArticleHtml = soup.select('ul li a')

for i in allArticleHtml :
   articleTextList.append(i.text)
   articleUrlList.append(i['href'])

# put each article in the list contentAll
c = 1
for i in articleUrlList :
   sb = ''
   content = requests.get(i, headers=headers)
   contentSoup = BeautifulSoup(content.text, 'html.parser')
   contentHtml = contentSoup.select('div .ndArticle_margin p') # it is a list of origin code of each article
   for j in contentHtml :
      sb += j.text
   contentAll.append(sb) # use this in jieba
   print('done',c)
   c += 1

for i in contentAll :
   print(i)
   print('----------------------------------')

# split each word in a single article , and put these words as one element in a list
# mapper
for i in contentAll :
   tmpWordAll = '/'.join(jieba.cut(i, cut_all=False)).split('/')
   wordEachArticle.append([j for j in tmpWordAll if len(j) > 1]) # see information in the head of the programe

# reduceer
for i in wordEachArticle :
   for j in i :
      if j not in wordCounter :
         wordCounter[j] = 1
      else :
         wordCounter[j] += 1

sb = ''
for key, value in wordCounter.items() :
   sb = sb + key + ('\t' if len(key) > 3 else '\t\t') + str(value) + '\n'
open('res\\map_reduce.txt', 'w', encoding = 'utf-8').write(sb)
open('res\\map_reduce.csv', 'w', encoding = 'utf-8').write(sb)

sb = ''
for key, value in wordCounter.items() :
   if value > 29 :
      sb = sb + key + ('\t' if len(key) > 3 else '\t\t') + str(value) + '\n'
open('res\\hot_words.txt', 'w', encoding = 'utf-8').write(sb)
open('res\\hot_words.csv', 'w', encoding = 'utf-8').write(sb)
