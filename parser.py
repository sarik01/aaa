import requests
from bs4 import BeautifulSoup as bs
page = 1
while True:
    r = requests.get('https://stopgame.ru/show/122612/impostor_factory_review#comments' + str(page))
    html = bs(r.content, 'html.parser')
    items = html.select(".page-layout > .page-content")
    if (len(items)):
        for el in items:
            title = el.select('.article >   p')
            print(title[0].text )
        page += 1
    else:
        break