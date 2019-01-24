import threading
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd
import os


def food(allRegionUrl ,start, end) :

    for regionNum in range(start, end):

        '''sb = 'English Name,Scores,Price,Payment,URL\n'
        open('E:\\python\\Crawler\\res\\food\\%s.csv' %(allRegionUrl[regionNum].text), 'w', encoding='utf-8').write(sb)
        '''
        #pd
        sbl = ['English Name','Scores','Price','Payment','URL']
        df = pd.DataFrame(columns=sbl)

        page = 1
        while True:

            print('--Page %s' % page)

            url = '%srstLst/%s/?SrtT=rt' % (allRegionUrl[regionNum]['href'], page)
            try:
                res = urlopen(url)
                soup = BeautifulSoup(res, 'html.parser')

                titleInfo = soup.select('div .list-rst__header a')
                titleLittle = soup.select('div .list-rst__header small')
                t = 0
                star = soup.select(
                    'div[class="list-rst__contents u-clearfix"] div[class="list-rst__info u-clearfix"] ul[class="list-rst__rate"] li b[class="c-rating__val"]')
                price = soup.select('ul[class="list-rst__price"] li span')
                payment = soup.select('div[class="list-rst__option"]')

                for i in titleInfo:
                    sb = ''

                    print(i.text, titleLittle[t].text)
                    score = 'Score [ Average : %s , Dinner : %s , Lunch : %s ]' % (
                    star[t * 1].text, star[t * 2].text, star[t * 3].text)
                    priceEach = 'Price [%s%s , %s%s]' % (
                    price[t * 2].text, price[t * 1].text, price[t * 4].text, price[t * 3].text)
                    paymentEach = 'Payment : ' + ('Credit card/Cash' if '信用卡' in payment[t].text else 'Cash only')
                    print(score)
                    print(priceEach)
                    print(paymentEach)
                    print(i['href'])
                    print('---')

                    score = 'Average:%s  Dinner:%s  Lunch:%s' % (star[t * 1].text, star[t * 2].text, star[t * 3].text)
                    priceEach = '%s%s  %s%s' % (
                    price[t * 2].text, price[t * 1].text, price[t * 4].text, price[t * 3].text)
                    paymentEach = 'Payment : ' + ('Credit card/Cash' if '信用卡' in payment[t].text else 'Cash only')

                    '''sb = '%s,%s,%s,%s,%s\n' % (
                    i.text.replace(',', ' '), score, priceEach.replace(',', '').replace('￥', '$').replace('～', '-'),
                    paymentEach, i['href'])
                    open('E:\\python\\Crawler\\res\\food\\%s.csv' % (allRegionUrl[regionNum].text), 'a', encoding='utf-8').write(sb)
                    '''
                    #pd
                    s = pd.Series([i.text.replace(',', ' '),
                                   score,
                                   priceEach.replace(',', '').replace('￥', '$').replace('～', '-'),
                                   paymentEach,
                                   i['href']],
                                  index=sbl)
                    df = df.append(s, ignore_index=True)
                    df.to_csv('E:\\python\\Crawler\\res\\food3\\%s.csv' % (allRegionUrl[regionNum].text), encoding='utf-8', index=False)

                    time.sleep(0.3)
                    t += 1

                print('---------')
                page += 1
                time.sleep(1)

            except:
                print('Error')
                time.sleep(30)
                break




allUrl = 'https://tabelog.com/tw/'
allRes = urlopen(allUrl)
allSoup = BeautifulSoup(allRes, 'html.parser')
allRegionUrl = allSoup.select('dd ul[class="index-area__list-items u-clearfix"] li a')

threadList = list()
for s in range(0,47) :
    threadList.append(threading.Thread(target=food, args = (allRegionUrl ,s, s+1)))

for i in threadList :
    i.start()



