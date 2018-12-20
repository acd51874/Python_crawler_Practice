import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import os
import ssl
import time

# used to fix Python SSL CERTIFICATE_VERIFY_FAILED
# for MacOS
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

x = 0 # file name
site = 230079000 # this can be changed
d = str(input("Select a drive you want to download the photo.(Please enter C, D or E.)\n"))
type = str(input("Which type of article you want to download?\n"))
countCheck = 0
count = 0

# count the amount of  photo
while countCheck != 1:
    site = 230079000
    count = int(input('How many pages do you want to survey?(There are 100 articles in each page.)\n'))
    countPhoto = 0
    print('Computing......')

    for i in range(0, count):
        url = 'https://www.dcard.tw/_api/forums/' + \
              type + \
              '/posts?popular=false&limit=100&before=%s'%site
        a = requests.get(url, headers = headers)
        soup = BeautifulSoup(a.text, 'html.parser')
        target = re.findall('https://i.imgur.com/[a-zA-Z0-9]*.jpg', soup.text)
        countPhoto += len(target)

        site -= 1000

    print('Threr are about %s photos.\n'%countPhoto)
    countCheck = int(input('Enter 1 to download, or enter 0 to re-set.\n'))

site = 230079000

print('Photos will be downloaded in %s:\\tem_py\\image_'%d+type)
print('')
print('Loading......\n')
time.sleep(5)

if not os.path.isdir('%s:\\tem_py'%d):
    os.mkdir('%s:\\tem_py'%d)
if not os.path.isdir('%s:\\tem_py\\image_'%d+type):
    os.mkdir('%s:\\tem_py\\image_'%d+type)

# download
for i in range(0, count):

    url = 'https://www.dcard.tw/_api/forums/' + \
          type + \
          '/posts?popular=false&limit=100&before=%s'%site
    a = requests.get(url, headers = headers)
    soup = BeautifulSoup(a.text, 'html.parser')
    target = re.findall('https://i.imgur.com/[a-zA-Z0-9]*.jpg', soup.text)

    for j in target:
        local = os.path.join(d + ':\\tem_py\\image_' + type + '\\%s.jpg' % x)
        urlretrieve(j, local)
        x += 1
        print(str(x) + '.jpg downloaded.')

    site -= 1000

print('\nAll done!')
print('Photos have been downloaded in %s:\\tem_py\\image_'%d+type)
time.sleep(10)