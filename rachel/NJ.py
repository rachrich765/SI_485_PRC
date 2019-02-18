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
first_link = soup.find("a", {"class": "BlogList-item-title"},  href=True)
#go to full page description of first item
url2 ='https://www.cyber.nj.gov/data-breach-alerts/20190102/caribou-coffee'
#'https://www.cyber.nj.gov' + str(first_link['href'])
res2 = requests.get(url2)
soup2 = BeautifulSoup(res2.content, 'html.parser')
#2 different methods for getting information from p tags, as html is not consistent
try:
	w = soup2.find_all('p', {'style': 'white-space: pre-wrap;'})
except: 
	w = soup2.find_all('p', {'style':'white-space: pre-wrap;'})

#if pdf link exists in paragraph, acquire link
links = []
for h in w:
	a = h.find('a', href=True)
	link = str(a['href'])
	if link.endswith('pdf'):
		links.append(link)
print(links)
for x in links:
	response = requests.get(link)
	my_raw_data = response.content
	#write pdf file for each link
	with open("new_pdf.pdf", 'wb') as my_data:
		my_data.write(my_raw_data)
	my_data.close() 
#read pdf file
pdf_file = open('new_pdf.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
#save pdf file contents to dictionary
nj_dict = page_content