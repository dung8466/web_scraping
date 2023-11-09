# -*- coding: utf8 -*-
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class Item:
    url: str
    name: str
    current_price: str
    place: str
    img: str


# conn = sqlite3.connect('../../db.sqlite3')
# c = conn.cursor()

# c.execute("CREATE TABLE IF NOT EXISTS products (url TEXT, name TEXT, current_price TEXT, prev_price TEXT, place TEXT, img TEXT)")

# start by defining the options
options = webdriver.ChromeOptions()
# it's more scalable to work in headless mode
options.add_argument("--headless")
# normally, selenium waits for all resources to download
# we don't need it as the page also populated with the running javascript code.
options.page_load_strategy = 'none'
# this returns the path web driver downloaded
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
# pass the defined options and service objects to initialize the web driver
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)


def cellphones(query):
    lists = []
    search = query.replace(' ', '%20')
    url = f"https://cellphones.com.vn/catalogsearch/result?q={search}"
    driver.get(url)
    content = driver.find_element(
        By.CSS_SELECTOR, "div[id*='search-catalog-page']")
    items = content.find_elements(
        By.CSS_SELECTOR, "div[class*='product-info']")
    i = 0
    for _ in items:
        if items.__len__() > 10:
            if i < 10:
                item = Item(
                    url=_.find_element(By.CSS_SELECTOR, "a").get_attribute('href'),
                    name=_.find_element(
                        By.CSS_SELECTOR, "h3").text,
                    current_price=_.find_element(
                        By.CSS_SELECTOR, "p[class*='product__price--show']").text,
                    place="Cellphones",
                    img=_.find_element(
                        By.CSS_SELECTOR, "img").get_attribute('src')
                )
                lists.append(item)
            else:
                break
            i += 1
        else:
            item = Item(
                url=_.find_element(By.CSS_SELECTOR, "a").get_attribute('href'),
                name=_.find_element(
                    By.CSS_SELECTOR, "h3").text,
                current_price=_.find_element(
                    By.CSS_SELECTOR, "p[class*='product__price--show']").text,
                place="Cellphones",
                img=_.find_element(
                    By.CSS_SELECTOR, "img").get_attribute('src')
            )
            lists.append(item)
    
    return lists
    #     c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?)",
    #                   (item.url, item.name, item.current_price, item.prev_price, item.place, item.img))
    # conn.commit()
    # conn.close()
