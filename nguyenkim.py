# -*- coding: utf8 -*-
import requests
from bs4 import BeautifulSoup as bs
import json
from rich import print
import base64


def gg_shopping(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }
    s = requests.Session()
    s.headers.update(headers)
    big_list = []
    search = query.replace(' ', '+')
    r = s.get(f'https://www.google.com/search?q={search}&tbm=shop')
    soup = bs(r.text, 'lxml')
    all_prods = soup.find_all('div', 'sh-dgr__gr-auto')
        # print(all_prods)
    for prod in all_prods:
        link = "https://www.google.com" + str(prod.find('a').get('href'))
        img = prod.find('img').get('src')
        img = img.split('base64,')[1]
        decoded = base64.decodebytes(img.encode("ascii"))
        print(decoded)

def main():
    gg_shopping("may tinh")

if __name__ == "__main__":
    main()