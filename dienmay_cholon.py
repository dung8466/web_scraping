# -*- coding: utf8 -*-
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from rich import print

@dataclass
class Item:
    url: str
    name: str
    current_price: str
    place: str
    img: str


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.page_load_strategy = 'none'
chrome_path = ChromeDriverManager().install()
chrome_service = Service(chrome_path)
driver = Chrome(options=options, service=chrome_service)
driver.implicitly_wait(5)

def dienmay_cholon(query):
    lists = []
    search = query.replace(' ', '-')
    url = f"https://dienmaycholon.vn/tu-khoa/{search}"
    print(url)
    driver.get(url)
    content = driver.find_element(By.CLASS_NAME, 'products')
    items = content.find_elements(
        By.CLASS_NAME, 'product')
    i = 0
    for _ in items:
        if items.__len__() > 10:
            if i < 10:
                item = Item(
                    url=_.find_element(By.CSS_SELECTOR, "a[class*='img_pro']").get_attribute('href'),
                    name=_.find_element(By.CSS_SELECTOR, 'h3 > span').text,
                    current_price=_.find_element(By.CSS_SELECTOR, "div.price_sale span").text,
                    place="Nguyen Kim",
                    img=_.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
                )
                print(item)
                lists.append(item)
            else:
                break
            i += 1
        else:
            item = Item(
                url=_.find_element(By.CSS_SELECTOR, "a[class*='img_pro']").get_attribute('href'),
                name=_.find_element(By.CSS_SELECTOR, 'h3 > span').text,
                current_price=_.find_element(By.CSS_SELECTOR, "div.price_sale span").text,
                place="Nguyen Kim",
                img=_.find_element(By.CSS_SELECTOR, "img").get_attribute('src')
            )
            lists.append(item)
    return lists

