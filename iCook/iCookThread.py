from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import time
import os
import threading


def editSingleCsv(i, j):
    startTime = time.time()
    dataCount = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    # Homepage with all categories
    resAll = requests.get('https://icook.tw/categories', headers=headers)
    soupAll = BeautifulSoup(resAll.text, 'html.parser')

    ## Get each category name and url
    # Category name -> categoryNameAll[2].select('h4 a')[0].text
    # Subcategory name -> categoryNameAll[2].select('div[class="panel-group"] a[class="list-title"]') -> i.text
    # Url of Subcategory -> categoryNameAll[2].select('div[class="panel-group"] a[class="list-title"]') -> i['href']
    categoryNameAll = soupAll.select(
        'div[class="inner-block"] div[class="entry"]')  # from [2] , name h4.a , div[class="panel-group"] a[class="list-title"]

    # The i_th category
    try:
        categoryName = categoryNameAll[i].select('h4 a')[0].text
        subCategoryList = categoryNameAll[i].select('div[class="panel-group"] a[class="list-title"]')
    except:
        print('list index out of range (i=%s)'%i)
        return 0

    # The j_th subcategory under the i_th category above
    try:
        subCategoryName = subCategoryList[j].text
        subCategoryUrl = 'https://icook.tw' + subCategoryList[j]['href']
    except:
        print('list index out of range (j=%s)'%j)
        return 0

    page = 1
    while True:
        try:
            # Each article(food) in the j_th subcategory above
            eachPageUrl = subCategoryUrl + '?page=%s' % page
            resEachPage = requests.get(eachPageUrl, headers=headers)
            print('resEachPage=%s , i=%s , j=%s , page=%s'%(resEachPage, i, j, page)) # Check if response is 200
            testTimes = 1
            while (str(resEachPage) != '<Response [200]>'):
                print('Trying requests again! (%s)'%resEachPage)
                time.sleep(10)
                resEachPage = requests.get(eachPageUrl, headers=headers)
                print('resEachPage=%s , i=%s , j=%s , page=%s' % (resEachPage, i, j, page))  # Check if response is 200
                if testTimes > 5:
                    break
                testTimes += 1
            soupEachPage = BeautifulSoup(resEachPage.text, 'html.parser')
            # Check if there is nothing
            if len(soupEachPage.select('a[class="browse-recipe-cover-link"]')) == 0:
                print('res/%s/%s.csv.....done (%s)!' % (categoryName, subCategoryName, dataCount))
                timeTook = time.time() - startTime
                with open('res/log.txt', 'a', encoding='utf-8') as f:
                    f.write('res/%s/%s.csv\nData : %s\nTime take : %s sec\n-\n' % (categoryName, subCategoryName, dataCount, timeTook))
                break
            # Get each cuisine name and url
            for k in soupEachPage.select('a[class="browse-recipe-cover-link"]'):
                eachCuisineUrl = 'https://icook.tw' + k['href']  # Url in csv
                eachCuisineName = k['title']  # Cuisine in csv
                resEachCuisine = requests.get(eachCuisineUrl, headers=headers)
                print('resEachCuisine=%s , i=%s , j=%s , page=%s , k=%s' % (resEachCuisine, i, j, page, k))  # Check if response is 200
                testTimes = 1
                while (str(resEachCuisine) != '<Response [200]>'):
                    print('Trying requests again! (%s)' % resEachCuisine)
                    time.sleep(10)
                    resEachCuisine = requests.get(eachCuisineUrl, headers=headers)
                    print('resEachPage=%s , i=%s , j=%s , page=%s' % (
                    resEachPage, i, j, page))  # Check if response is 200
                    if testTimes > 10:
                        break
                    testTimes += 1
                soupEachCuisine = BeautifulSoup(resEachCuisine.text, 'html.parser')
                # Ingredients in csv
                ingredientName = soupEachCuisine.select('div[class="ingredient-name"]')
                ingredientUnit = soupEachCuisine.select('div[class="ingredient-unit"]')
                ingredient = ''
                for m in range(0, len(ingredientName)):
                    ingredient += '{%s:%s}' % (ingredientName[m].text, ingredientUnit[m].text)
                # Process in csv
                #
                # Image in csv
                image = soupEachCuisine.select('img[class="main-pic"]')[0]['src']

                with open('res/%s/%s.csv' % (categoryName, subCategoryName), 'a', encoding='utf-8') as f:
                    f.write('%s,%s,%s,%s\n' % (eachCuisineName, ingredient, image, eachCuisineUrl))
                print('res/%s/%s.csv successfully appended!'% (categoryName, subCategoryName))
                dataCount += 1
                time.sleep(1)

            page += 1
        except:
            print('error : res/%s/%s.csv.....done!' % (categoryName, subCategoryName))
            time.sleep(30)
            break

    print('-')


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

# Homepage with all categories
resAll = requests.get('https://icook.tw/categories', headers=headers)
soupAll = BeautifulSoup(resAll.text, 'html.parser')

## Get each category name and url
# Category name -> categoryNameAll[2].select('h4 a')[0].text
# Subcategory name -> categoryNameAll[2].select('div[class="panel-group"] a[class="list-title"]') -> i.text
# Url of Subcategory -> categoryNameAll[2].select('div[class="panel-group"] a[class="list-title"]') -> i['href']
categoryNameAll = soupAll.select(
    'div[class="inner-block"] div[class="entry"]')  # from [2] , name h4.a , div[class="panel-group"] a[class="list-title"]

# mkdir and csv_column
os.mkdir('res')
for i in range(2, len(categoryNameAll)):

    # Each category
    categoryName = categoryNameAll[i].select('h4 a')[0].text

    # mkdir : named by category
    os.mkdir('res/%s' % categoryName)

    for j in categoryNameAll[i].select('div[class="panel-group"] a[class="list-title"]'):
        # Each subcategory under the category above
        subCategoryName = j.text
        subCategoryUrl = 'https://icook.tw' + j['href']

        # csv : named by subcategory
        with open('res/%s/%s.csv' % (categoryName, subCategoryName), 'w', encoding='utf-8') as f:
            f.write('Cuisine,Ingredients,Image,Url\n')

# log
with open('res/log.txt', 'w', encoding='utf-8') as f:
    f.write('')

threadList = list()
for i in range(2, len(categoryNameAll)):
    subCategoryList = categoryNameAll[i].select('div[class="panel-group"] a[class="list-title"]')
    for j in range(0, len(subCategoryList)):
        threadList.append(threading.Thread(target=editSingleCsv, args=(i, j)))

for i in threadList:
    i.start()
    time.sleep(1)

print('\n==========\n%s threads running.\n==========\n'%len(threadList))