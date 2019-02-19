import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh
import re
import PyPDF2

links = []
description_links = list()
url = 'https://www.cyber.nj.gov/data-breach-alerts'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
#get first item in list of postings
titles = soup.find_all("section", {"class": "BlogList BlogList--posts-excerpt sqs-blog-list clear"})
for t in titles:
	description_links1 = t.find_all('a', {'class':'BlogList-item-title'}, href=True)
	for d in description_links1:
		description_link = d['href']
		description_links.append(description_link)
	for dl in description_links:
		url2 = 'https://www.cyber.nj.gov' + str(dl)
		res2 = requests.get(url2)
		soup2 = BeautifulSoup(res2.content, 'html.parser')
		try:
			w = soup2.find_all('p', {'style': 'white-space: pre-wrap;'})
		except: 
			w = soup2.find_all('p', {'style':'white-space: pre-wrap;'})
		else:
			w = soup2.find_all('p')
		#if pdf link exists in paragraph, acquire link
		for h in w:
			a = h.find('a', href=True)
			if a:
				link = str(a['href'])
				if link.endswith('pdf'):
					links.append(link)

read_more = soup.find_all("a", {"class": "BlogList-pagination-link"})
for rm in read_more:
	if rm['href']:
		url3 = 'https://www.cyber.nj.gov'  + str(rm['href'])
		res3 = requests.get(url3)
		soup3 = BeautifulSoup(res3.content, 'html.parser')
print(links)