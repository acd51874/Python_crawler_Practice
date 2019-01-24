import requests
import json

url = 'https://crazy.ck101.com/category/more'
postData = {'id' : 1, 'page' : 2}
res = requests.post(url, data=postData)
news = json.loads(res.text)

for i in news:
    print('Title:\t' + i['title'])
    print('URL:\t' + 'https://crazy.ck101.com/post/%s'%i['id'])
    print('-')

