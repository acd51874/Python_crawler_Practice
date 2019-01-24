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
    os.mkdir('res/%s'%categoryName)

    for j in categoryNameAll[i].select('div[class="panel-group"] a[class="list-title"]'):

        # Each subcategory under the category above
        subCategoryName = j.text
        subCategoryUrl = 'https://icook.tw' + j['href']

        # csv : named by subcategory
        with open('res/%s/%s.csv'%(categoryName, subCategoryName), 'w', encoding='utf-8') as f:
            f.write('Cuisine,Ingredients,Image,Url\n')


# edit csv
for i in range(2, len(categoryNameAll)):
    # Each category
    categoryName = categoryNameAll[i].select('h4 a')[0].text
    print(categoryNameAll[i].select('h4 a')[0].text)
    print('===')
    subCategoryList = categoryNameAll[i].select('div[class="panel-group"] a[class="list-title"]')
    for j in range(0, len(subCategoryList)):
        # Each subcategory under the category above
        subCategoryName = subCategoryList[j].text
        subCategoryUrl = 'https://icook.tw' + subCategoryList[j]['href']
        print(subCategoryName)
        print(subCategoryUrl)
        page = 1
        while True:
            try:
                # Each article(food) in the subcategory above
                eachPageUrl = subCategoryUrl + '?page=%s'%page
                resEachPage = requests.get(eachPageUrl, headers=headers)
                soupEachPage = BeautifulSoup(resEachPage.text, 'html.parser')
                # Check if there is nothing
                if len(soupEachPage.select('a[class="browse-recipe-cover-link"]')) == 0:
                    print('res/%s/%s.csv.....done!' % (categoryName, subCategoryName))
                    break
                # Get each cuisine name and url
                for k in soupEachPage.select('a[class="browse-recipe-cover-link"]'):
                    eachCuisineUrl = 'https://icook.tw' + k['href'] # Url in csv
                    eachCuisineName = k['title'] # Cuisine in csv
                    resEachCuisine = requests.get(eachCuisineUrl, headers=headers)
                    soupEachCuisine = BeautifulSoup(resEachCuisine.text, 'html.parser')
                    # Ingredients in csv
                    ingredientName = soupEachCuisine.select('div[class="ingredient-name"]')
                    ingredientUnit = soupEachCuisine.select('div[class="ingredient-unit"]')
                    ingredient = ''
                    for m in range(0, len(ingredientName)):
                        ingredient += '{%s:%s}'%(ingredientName[m].text, ingredientUnit[m].text)
                    # Process in csv
                    #
                    # Image in csv
                    image = soupEachCuisine.select('img[class="main-pic"]')[0]['src']

                    with open('res/%s/%s.csv'%(categoryName, subCategoryName), 'a', encoding='utf-8') as f:
                        f.write('%s,%s,%s,%s\n'%(eachCuisineName, ingredient, image, eachCuisineUrl))

                page += 1
            except:
                print('res/%s/%s.csv.....done!'%(categoryName, subCategoryName))
                break

        print('-')
    print('===')
