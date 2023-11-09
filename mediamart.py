from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def gg_shopping(query):
  search = query.replace(' ', '+')
  url = f'https://www.google.com/search?q={search}&tbm=shop'
  driver.get(url)
  images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.sh-dgr__gr-auto img[src]')))
  for image in images:
    print(image.get_property('src'))

gg_shopping('cat')