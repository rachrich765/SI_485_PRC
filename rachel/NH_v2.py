import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh
import urllib
import PyPDF2 
import os
import csv
import datefinder
from dateutil.parser import parse

NH_dict = dict()
links = list()
new_links = list()
letter_links = list()


url = 'https://www.doj.nh.gov/consumer/security-breaches/'

res = requests.get(url)

soup = BeautifulSoup(res.content, 'html.parser')

all_p = (soup.find_all('p'))

for p in all_p:
	letter_links_a = (p.find_all('a', href=True))
	for x in letter_links_a:
		letter_links.append(x['href'])

for x in letter_links:
	url2 = url + x
	res2 = requests.get(url2)
	soup2 = BeautifulSoup(res2.content, 'html.parser')
	a = soup2.find_all('a', href=True)
	for a2 in a:
		link = str(a2['href'])
		if link.endswith('pdf'):
			links.append('https://www.doj.nh.gov/consumer/security-breaches/' + link)


for l in links:
	response = requests.get(l)
	my_raw_data = response.content
	with open("new_pdf.pdf", 'wb') as my_data:
		my_data.write(my_raw_data)
		my_data.close()
	file = textract.process('new_pdf.pdf', method='pdfminer')
	NH_dict[l] = file
	os.remove("new_pdf.pdf")


end_time = time.time()
minutes = (end_time - start_time)/60
print("minutes:", minutes)


