from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import time
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

os.mkdir('res')
with open('res/7funsList.csv', 'w', encoding='utf-8') as f:
    f.write('Cuisine,Ingredients,Image,Url\n')

page = 1
for i in range(1, 3171):
    allPagesUrl = 'https://www.7funs.com/recipes/%s'%page
    resAll = requests.get(allPagesUrl, headers=headers)
    soupAll = BeautifulSoup(resAll.text, 'html.parser')
    try:
        cuisineName = soupAll.select('div[class="top_toole"] span')[0].text
        ingredientList = soupAll.select('div[class="Rbox"] ul p')
        ingredientName = ''
        for j in ingredientList:
            ingredientName += '{%s}'%j.text if (j.text != '食料：' and j.text != '調味料：') else ''
        imageUrl = soupAll.select('div[class="photo DBox_xx"] img')[0]['src']
        imageUrl = imageUrl if imageUrl != '' else 'none'
        print(cuisineName)
        print(ingredientName)
        print(imageUrl)
        with open('res/7funsList.csv', 'a', encoding='utf-8') as f:
            f.write('%s,%s,%s,%s\n'%(cuisineName.replace(',',';'), ingredientName.replace(',',';'), imageUrl, allPagesUrl))
        print('-')
    except:
        print('', end='')
    page += 1