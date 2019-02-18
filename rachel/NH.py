import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh

NH_dict = dict()
url = 'https://www.doj.nh.gov/consumer/security-breaches/'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
all_p = (soup.find_all('p'))
letter_links = list()
for p in all_p:
	letter_links_a = (p.find_all('a', href=True))
	if letter_links_a:
		#only get links for A-Z
		for x in letter_links_a[:-1]:
			letter_links.append(x['href'])

links = list()
for x in letter_links:
	url2 = url + x
	res2 = requests.get(url2)
	soup2 = BeautifulSoup(res2.content, 'html.parser')
	a = soup2.find_all('a', href=True)
	for a2 in a:
		link = str(a2['href'])
		if link.endswith('pdf'):
			links.append(link)
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
NH_dict = page_content
