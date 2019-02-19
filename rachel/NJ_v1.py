import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh
import re
import PyPDF2
nj_dict = {}
url = 'https://www.cyber.nj.gov/data-breach-alerts'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
#get first item in list of postings
first_link = soup.find("section", {"class": "BlogList BlogList--posts-excerpt sqs-blog-list clear"},  href=True)

#go to full page description of first item
url2 ='https://www.cyber.nj.gov' + str(first_link['href'])
res2 = requests.get(url2)
soup2 = BeautifulSoup(res2.content, 'html.parser')
#2 different methods for getting information from p tags, as html is not consistent
try:
	w = soup2.find_all('p', {'style': 'white-space: pre-wrap;'})
except: 
	w = soup2.find_all('p', {'style':'white-space: pre-wrap;'})
else:
	w = soup2.find_all('p')

#if pdf link exists in paragraph, acquire link
links = []
for h in w:
	a = h.find('a', href=True)
	if a:
		link = str(a['href'])
		if link.endswith('pdf'):
			links.append(link)

next_page = soup2.find('a', {'class': 'BlogItem-pagination-link BlogItem-pagination-link--next'}, href=True)
url3 = 'https://www.cyber.nj.gov' + str(next_page['href'])
res3 = requests.get(url3)
soup3 = BeautifulSoup(res3.content, 'html.parser')
# #2 different methods for getting information from p tags, as html is not consistent
try:
	w2 = soup3.find_all('p', {'style': 'white-space: pre-wrap;'})
except: 
	w2 = soup3.find_all('p', {'style':'white-space: pre-wrap;'})
for h in w2:
	a = h.find('a', href=True)
	#if pdf link in p tag, append it to the list
	if a:
		link = str(a['href'])
		if link.endswith('pdf'):
			links.append(link)
	#if no pdf link in p tag, go to next page
	else:
		next_page = soup3.find('a', {'class': 'BlogItem-pagination-link BlogItem-pagination-link--next'}, href=True)
		if next_page:
			url4 = 'https://www.cyber.nj.gov' + str(next_page['href'])
			res4 = requests.get(url4)
			soup4 = BeautifulSoup(res4.content, 'html.parser')
			try:
				w3 = soup4.find_all('p', {'style': 'white-space: pre-wrap;'})
			except: 
				w3 = soup4.find_all('p', {'style':'white-space: pre-wrap;'})
			for h in w3:
				a = h.find('a', href=True)
				#if pdf link in p tag, append it to the list
				if a:
					link = str(a['href'])
					if link.endswith('pdf'):
						links.append(link)
print(links)