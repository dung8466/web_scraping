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


def cellphones(query):
    lists = []
    search = query.replace(' ', '+')
    gg_url = f"https://www.google.com/search?q=dien+may+xanh+{search}&num=1"
    driver.get(gg_url)
    link = driver.find_element(By.CSS_SELECTOR, '#rso > div > div > div > div > div.kb0PBd.cvP2Ce.jGGQ5e > div > div > span > a').get_attribute('href')
    driver.get(link)
    content = driver.find_element(By.CSS_SELECTOR, "section[id='categoryPage']")
    items = content.find_elements(By.CSS_SELECTOR, "li[class*='item']")
    i = 0
    for _ in items:
        if items.__len__() > 10:
            if i < 10:
                item = Item(
                    url=_.find_element(By.TAG_NAME, "a").get_attribute('href'),
                    name=_.find_element(
                        By.TAG_NAME, "h3").text,
                    current_price=_.find_element(
                        By.CSS_SELECTOR, "strong[class*='price']").text,
                    place="Điện máy xanh",
                    img=_.find_element(
                        By.TAG_NAME, "img").get_attribute('src')
                )
                lists.append(item)
            else:
                break
            i += 1
        else:
            item = Item(
                url=_.find_element(By.TAG_NAME, "a").get_attribute('href'),
                name=_.find_element(
                    By.TAG_NAME, "h3").text,
                current_price=_.find_element(
                    By.CSS_SELECTOR, "strong[class*='price']").text,
                place="Điện máy xanh",
                img=_.find_element(
                    By.TAG_NAME, "img").get_attribute('src')
                )
                lists.append(item)
    print(lists)
    driver.close()


def main():
    cellphones('may tinh')


if __name__ == '__main__':
    main()
