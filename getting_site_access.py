
import time
from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://www.nytimes.com/games/wordle/index.html'
driver.get(url)
button = driver.find_element_by_tag_name('body')
time.sleep(0.5)
button.click()

button.send_keys('q')
