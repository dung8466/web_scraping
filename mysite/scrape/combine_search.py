# -*- coding: utf8 -*-
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from rich import print
import requests
from bs4 import BeautifulSoup as bs
import json
import sqlite3
from unidecode import unidecode
import datetime
from .models import *
from decimal import Decimal
from django.utils import timezone

@dataclass
class Item:
    url: str
    name: str
    current_price: Decimal
    place: str
    img: str
    date_add: datetime.datetime

userAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.56 Safari/537.36"
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument(f'user-agent={userAgent}')
options.page_load_strategy = 'none'
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 5)



def cellphones(query):
    # query = unidecode(query)
    lists = []
    search = query.replace(' ', '%20')
    url = f"https://cellphones.com.vn/catalogsearch/result?q={search}"
    driver.get(url)
    # content = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[id*='search-catalog-page']")))
    content = driver.find_element(
        By.CSS_SELECTOR, "div[id*='search-catalog-page']")
    items = content.find_elements(
        By.CSS_SELECTOR, "div[class*='product-info']")
    print(items)
    for _ in items:
    # _ = items[0]
        try:
            a = _.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            b = _.find_element(By.CSS_SELECTOR, "h3").text
            c = _.find_element(By.CSS_SELECTOR, "p[class*='product__price--show']").text
            d = _.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
            e = datetime.datetime.now(tz=timezone.utc)
            if c == "Giá Liên Hệ":
                c = Decimal("0")
            else:
                c = Decimal(c.replace("₫", "").replace(".","").replace(" ",""))
            item = Item(
                url=a,
                name=b,
                current_price=c,
                place="Cellphones",
                img=d,
                date_add=e
            )
            print(item)
            item_instance, created = Product.objects.update_or_create(
                name=item.name,
                place=item.place,
                defaults={
                    'current_price': item.current_price,
                    'url': item.url,
                    'img': item.img,
                    'date_add': item.date_add
                }
            )
            if not created:
                # Check if the current price is different from the previous price
                if item_instance.current_price != item.current_price:
                # Record price change
                    record_price_change(item_instance, item.current_price)
            else:
                # Record price change
                # record_price_change(item, item.current_price)
                price_history = PriceHistory(product=item, price=item.current_price, date=item.date_add)
                price_history.save()
            if any(obj.name == item.name for obj in lists):
                pass
            else:
                # lists.append(item)
                lists.append(item_instance)
        except:
            pass
    return lists

def media_mart(query):
    # query = unidecode(query)
    lists = []
    search = query.replace(' ', '+')
    url = f"https://mediamart.vn/tag?key={search}"
    driver.get(url)
    content = driver.find_element(By.CLASS_NAME, 'product-list-bycate')
    items = content.find_elements(
        By.CLASS_NAME, 'card')
    for _ in items:
    # _ = items[0]
        try:
            item = Item(
                url=_.find_element(By.CSS_SELECTOR, "a[class*='product-item']").get_attribute('href'),
                name=_.find_element(By.CSS_SELECTOR, "p[class*='card-title']").text,
                current_price=Decimal(_.find_element(By.CSS_SELECTOR, "p[class*='card-text']").text.replace("₫", "").replace(".","").replace(" ","")),
                place="Media Mart",
                img=_.find_element(By.CSS_SELECTOR, "img").get_attribute('src'),
                date_add=datetime.datetime.now(tz=timezone.utc)
            )
            item_instance, created = Product.objects.update_or_create(
                name=item.name,
                place=item.place,
                defaults={
                    'current_price': item.current_price,
                    'img': item.img,
                    'url': item.url,
                    'date_add': item.date_add
                }
            )
            if not created:
                # Check if the current price is different from the previous price
                if item_instance.current_price != item.current_price:
                # Record price change
                    record_price_change(item_instance, item.current_price)
            else:
                # Record price change
                price_history = PriceHistory(product=item, price=item.current_price, date=item.date_add)
                price_history.save()
            # lists.append(item)
            lists.append(item_instance)
        except:
            pass
    return lists

def nguyen_kim(query):
    # query = unidecode(query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }
    s = requests.Session()
    s.headers.update(headers)
    big_lists = []
    search = query.replace(' ', '+')
    for i in range(1, 3):
        r = s.get(f'https://www.nguyenkim.com/tim-kiem.html?tu-khoa={search}&trang={i}')
        soup = bs(r.text, 'lxml')
        all_prods = soup.select('script[class="script-render"]')
        # print(all_prods)
        for prod in all_prods:
        # _ = all_prods[0]
            try:
                prod_data = json.loads(prod.string.split('dataRenderProduct.push(')[1].split(');')[0])
                item = Item(
                    name=prod_data["display_name"],
                    url=prod_data["link"],
                    current_price=Decimal(prod_data["final_price_int"]),
                    # current_price=Decimal(prod_data["final_price"].replace("đ", "").replace(".","").replace(" ","")),
                    place="Nguyễn Kim",
                    img=prod_data["image_url"],
                    date_add=datetime.datetime.now(tz=timezone.utc)
                )
                item_instance, created = Product.objects.update_or_create(
                    name=item.name,
                    place=item.place,
                    defaults={
                        'current_price': item.current_price,
                        'img': item.img,
                        'url': item.url,
                        'date_add': item.date_add
                    }
                )
                if not created:
                    # Check if the current price is different from the previous price
                    if item_instance.current_price != item.current_price:
                    # Record price change
                        record_price_change(item_instance, item.current_price)
                else:
                # Record price change
                    price_history = PriceHistory(product=item, price=item.current_price, date=item.date_add)
                    price_history.save()
                # big_list.append(item)
                big_lists.append(item_instance)
                print(big_lists)
            except:
                pass
    return big_lists

def gg_shopping(query):
  search = query.replace(' ', '+')
  big_list = []
  url = f'https://www.google.com/search?q={search}&tbm=shop'
  driver.get(url)
  products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sh-dgr__gr-auto')))
  for product in products:
    try:
        item = Item(
            url=product.find_element(By.CSS_SELECTOR, "a").get_attribute('href'),
            name=product.find_element(By.CSS_SELECTOR, "h3[class*='tAxDx']").text,
            # current_price=Decimal(0),
            # current_price=(product.find_element(By.CSS_SELECTOR, "span.QIrs8 span").text.replace("₫", "").replace(".","").replace(" ","")),
            current_price=Decimal(product.find_element(By.CSS_SELECTOR, "span[class*='a8Pemb OFFNJ']").text.replace("₫", "").replace(".","").replace(" ","")),
            place=product.find_element(By.CSS_SELECTOR, "div[class*='aULzUe IuHnof']").text,
            img=product.find_element(By.CSS_SELECTOR, "img").get_attribute('src'),
            date_add=datetime.datetime.now(tz=timezone.utc)
        )
        item_instance, created = Product.objects.update_or_create(
            name=item.name,
            place=item.place,
            defaults={
                'current_price': item.current_price,
                'img': item.img,
                'url': item.url,
                'date_add': item.date_add
            }
        )
        if not created:
            # Check if the current price is different from the previous price
            if item_instance.current_price != item.current_price:
            # Record price change
                record_price_change(item_instance, item.current_price)
        else:
                # Record price change
            price_history = PriceHistory(product=item, price=item.current_price, date=item.date_add)
            price_history.save()
        # big_list.append(item)
        big_list.append(item_instance)
    except:
        pass
  return big_list

def cellphones_one(query):
    lists = []
    search = query.replace(' ', '%20')
    url = f"https://cellphones.com.vn/catalogsearch/result?q={search}"
    driver.get(url)
    content = driver.find_element(
        By.CSS_SELECTOR, "div[id*='search-catalog-page']")
    items = content.find_elements(
        By.CSS_SELECTOR, "div[class*='product-info']")
    
    # Check if there are items found
    if items:
        _ = items[0]
        # try:
        #     a = _.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        #     b = _.find_element(By.CSS_SELECTOR, "h3").text
        #     c = _.find_element(By.CSS_SELECTOR, "p[class*='product__price--show']").text
        #     d = _.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
        try:
            a = _.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
            b = _.find_element(By.CSS_SELECTOR, "h3").text
            c = _.find_element(By.CSS_SELECTOR, "p[class*='product__price--show']").text
            d = _.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
            e = datetime.datetime.now(tz=timezone.utc)
            if c == "Giá Liên Hệ":
                c = Decimal("0")
            else:
                c = Decimal(c.replace("₫", "").replace(".","").replace(" ",""))
            # Create a dictionary with the scraped data and add it to the temporary list
            item = Item(
                name=b,
                current_price=c,
                place="Cellphones",
                img=d,
                url=a,
                date_add=e
            )
            return [item]
        except:
            pass
    return []

def media_mart_one(query):
    lists = []
    search = query.replace(' ', '+')
    url = f"https://mediamart.vn/tag?key={search}"
    driver.get(url)
    content = driver.find_element(By.CLASS_NAME, 'product-list-bycate')
    items = content.find_elements(
        By.CLASS_NAME, 'card')

    # Check if there are items found
    if items:
        _ = items[0]
        try:
            item = Item(
                name=_.find_element(By.CSS_SELECTOR, "p[class*='card-title']").text,
                url= _.find_element(By.CSS_SELECTOR, "a[class*='product-item']").get_attribute('href'),
                current_price=Decimal(_.find_element(By.CSS_SELECTOR, "p[class*='card-text']").text.replace("₫", "").replace(".", "").replace(" ", "")),
                place="Media Mart",
                img=_.find_element(By.CSS_SELECTOR, "img").get_attribute('src'),
                date_add=datetime.datetime.now(tz=timezone.utc)
            )
            return [item]
        except:
            pass
    return []

def nguyen_kim_one(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }
    s = requests.Session()
    s.headers.update(headers)
    search = query.replace(' ', '+')
    r = s.get(f'https://www.nguyenkim.com/tim-kiem.html?tu-khoa={search}&trang=1')
    soup = bs(r.text, 'lxml')
    all_prods = soup.select('script[class="script-render"]')
    
    if all_prods:
        try:
            prod_data = json.loads(all_prods[0].string.split('dataRenderProduct.push(')[1].split(');')[0])
            item = Item(
                name=prod_data["display_name"],
                url=prod_data["link"],
                current_price=Decimal(prod_data["final_price_int"]),
                place="Nguyễn Kim",
                img=prod_data["image_url"],
                date_add=datetime.datetime.now(tz=timezone.utc)
            )
            return [item]
        except:
            pass
    return []

# Function to record price change
def record_price_change(product, new_price):
    # Retrieve the current price from the database
    current_price = product.current_price
    date = datetime.datetime.now(tz=timezone.utc)
    # Compare the current price with the new price
    if current_price != new_price:
        # Price has changed, record it
        price_history = PriceHistory(product=product, price=new_price, date=date)
        price_history.save()

def scrape_fake_product(query):
    lists = []
    url = "https://dung8466.github.io/fake_site/"
    driver.get(url)
    content = driver.find_element(By.ID, 'product-container')
    print(content)
    try:
        a = content.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        b = content.find_element(By.CSS_SELECTOR, "h1").text
        c = Decimal(content.find_element(By.CSS_SELECTOR, "p[id*='product-price']").text)
        d = content.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
        item = Item (
            url = a,
            name = b,
            current_price = c,
            place = "Fake",
            img = d,
            date_add = datetime.datetime.now(tz=timezone.utc)
        )
        item_instance, created = Product.objects.update_or_create(
            name=item.name,
            place=item.place,
            defaults={
                'current_price': item.current_price,
                'img': item.img,
                'url': item.url,
                'date_add': item.date_add
            }
        )
        if not created:
                # Check if the current price is different from the previous price
            if item_instance.current_price != item.current_price:
                # Record price change
                record_price_change(item_instance, item.current_price)
        else:
                # Record price change
            record_price_change(item, item.current_price)
        lists.append(item_instance)
    except:
        pass
    return lists

def scrape_fake_product_one(query):
    lists = []
    url = "https://dung8466.github.io/fake_site/"
    driver.get(url)
    content = driver.find_element(By.ID, 'product-container')
    try:
        a = content.find_element(By.CSS_SELECTOR, "a").get_attribute('href')
        b = content.find_element(By.CSS_SELECTOR, "h1").text
        c = Decimal(content.find_element(By.CSS_SELECTOR, "p[id*='product-price']").text)
        d = content.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
        item = Item (
            url = a,
            name = b,
            current_price = c,
            place = "Fake",
            img = d,
            date_add = datetime.datetime.now(tz=timezone.utc)
        )
        record_price_change(item, item.current_price)
        lists.append(item)
    except:
        pass
    return lists