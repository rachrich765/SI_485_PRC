import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh
import re
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

NJ_dict = dict()
driver = webdriver.Chrome()
links = []
description_links = list()
url = 'https://www.cyber.nj.gov/data-breach-alerts'

res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
#get first item in list of postings
a=soup.find("section", {"class": "BlogList BlogList--posts-excerpt sqs-blog-list clear"})
x = a.find('a', href=True)
link = x['href']
url2 = 'https://www.cyber.nj.gov' + str(link)
res2 = requests.get(url2)
soup2 = BeautifulSoup(res2.content, 'html.parser')
driver.get(url2)
b = soup2.find("a", {"class":"BlogItem-pagination-link BlogItem-pagination-link--next"}, href=True)
link2 = b.get('href')

pdf_urls = list()
#close popup window
time.sleep(5)
python_button = driver.find_element_by_xpath("//a[@class='sqs-popup-overlay-close']").click()

while True:
	try:
		pdfs = driver.find_elements_by_xpath("//a[contains(@href, '.pdf')]")
		for pdf in pdfs:
			link = pdf.get_attribute("href")
			if link not in pdf_urls:
				pdf_urls.append(link)
		python_button2 = driver.find_element_by_xpath("//a[@class='BlogItem-pagination-link BlogItem-pagination-link--next']").click()
	except:
		break
	

for pdf_url in pdf_urls:
	response = requests.get(pdf_url)
	my_raw_data = response.content
	with open("new_pdf.pdf", 'wb') as my_data:
		my_data.write(my_raw_data)
		my_data.close()
	file = textract.process('new_pdf.pdf', method='pdfminer')
	NJ_dict[pdf_url] = file
	os.remove("new_pdf.pdf")

end_time = time.time()
print("minutes",(end_time - start_time)/60)