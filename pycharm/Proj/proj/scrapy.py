import time
import requests
from bs4 import BeautifulSoup
from proj.tasks import get_content

t1 = time.time()
url = "http://www.wikidata.org/w/index.php?title=Special:WhatLinksHere/Q5limit=500&from=0"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36(KHTML,like Gecko)\
           Chrome/67.0.3396.87 Safari/537.36'}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")
human_list = soup.find(id='mw-whatlinkshere-list')('li')

urls = []
for human in human_list:
    url = human.find('a')['href']
    urls.append('https://www.wikidata.org'+url)

result = get_content.delay(urls)
res = [v for v in result.collect()]
for r in res:
    if isinstance(r[1], list) and isinstance(r[1][0], str):
        print(r[1])

t2 = time.time()
print('耗时:%s' % (t2-t1))