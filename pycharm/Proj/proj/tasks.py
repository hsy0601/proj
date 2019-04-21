import re
import requests
from celery import group
from proj.app_test import app

@app.task(trail=True)
def get_content(urls):
    return group(C.s(url) for url in urls)()

@app.task(trail=True)
def C(url):
    return parser.delay(url)

@app.task(trail=True)
def parser(url):
    req = requests.get(url)
    html = req.text
    try:
        name = re.findall(r'<span class="wikibase-title-label">(.+?)</span>', html)[0]
        desc = re.findall(r'<span class="wikibase-descriptionview-text">(.+?)</span>', html)[0]
        if name is not None and desc is not None:
            return name.desc
    except Exception as err:
        return '', ''
