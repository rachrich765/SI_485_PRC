import time
start_time = time.time()

import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

tables1 = list()
driver = webdriver.Chrome()
driver.get(url)


python_button = driver.find_elements_by_xpath("//a[@class='ui-paginator-page ui-state-default ui-corner-all']")
buttons = len(python_button)
for i in range(buttons):
	python_button = driver.find_elements_by_xpath("//a[@class='ui-paginator-page ui-state-default ui-corner-all']")
	x = python_button[i]
	x.click()
	time.sleep(5)
	y = driver.page_source
	tables = pd.read_html(y, header=0)
	data_USDHHSOCR = tables[1]

end_time = time.time()
minutes = (end_time - start_time)/60
print("minutes:", minutes)