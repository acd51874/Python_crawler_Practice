from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import time
import threading
import os

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

'''url = 'https://www.ptt.cc/bbs/Gossiping/M.1547006323.A.12E.html'
session = requests.Session()
res = session.get(url, cookies={'over18':'1'})
soup = BeautifulSoup(res.text, 'html.parser')
'''

def pullArticle(page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    url = 'https://www.ptt.cc/bbs/Gossiping/index%s.html'%(page)
    ss = requests.session()
    ss.cookies['over18'] = '1'
    res = ss.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')


    '''r = Request(url)
    r.add_header('user-agent', 'Mozilla/5.0')
    res = urlopen(r)
    soup = BeautifulSoup(res, 'html.parser')
    '''

    with open('resGossip/%s.txt' % (page), 'w', encoding='utf-8') as f:
        f.write('')

    # title list (name and url)
    titleList = soup.select('div[class="title"] a')
    for i in range(0, len(titleList)):

        titleName = titleList[i].text
        titleUrl = 'https://www.ptt.cc' + titleList[i]['href']

        resArticle = ss.get(titleUrl, headers=headers)
        soupArticle = BeautifulSoup(resArticle.text, 'html.parser')
        articleList = soupArticle.select('div[id="main-content"]')
        #articleInfo = articleList.select('div[class="article-meta-value"]')
        # // *[ @ id = "main-content"] / text()[1]
        try:
            articleContent = articleList[0].text.split('--')[0]
        except:
            print('IndexError: list index out of range')

        score = 0
        pushTagList = soupArticle.select('div[class="push"] span')
        for j in pushTagList:
            if '推 ' in j.text:
                score += 1
            if '噓' in j.text:
                score -= 1

        print('[Score : %s]'%score, titleName)
        print(titleUrl)
        print(articleContent)
        print('-')

        with open('resGossip/%s.txt'%(page), 'a', encoding='utf-8') as f:
            f.write('[Score : %s] '%score + titleName + '\n' + titleUrl + '\n\n' + articleContent + '\n-\n-\n')

os.mkdir('resGossip')

threadList = list()
for i in range(39201, 1, -1):
    threadList.append(threading.Thread(target=pullArticle, args=(i,)))

for i in threadList:
    time.sleep(0.15)
    i.start()


'''for i in range(1, 7435):
    pullArticle(i)
'''
#pullArticle(39200)
'''with requests.Session() as s:
    s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
'''