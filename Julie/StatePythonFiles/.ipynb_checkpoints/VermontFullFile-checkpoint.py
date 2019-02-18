#472.70189118385315 seconds
#just under 8 min

import requests
import textract
import os

from bs4 import BeautifulSoup
url = 'https://ago.vermont.gov/archived-security-breaches/'
code = requests.get(url)
plain = code.text
s = BeautifulSoup(plain, "html.parser")

year_urls= []
for x in s('li', {'class':"awDatesLI"}):
    for item in x('a'):
        year_urls.append(item.get('href'))

import time
start_time = time.time()

vermont_dict = {}

for year in year_urls:
    vermont_dict[year[-4:]] = {}
    breaches = []
    code = requests.get(year)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")

    for x in s('div', {'id':"postWrapper"}):
        for item in x('a'):
            breaches.append((item('h3',{'class':'awyca_subheader'})[0].text,item.get('href')))

    for breach in breaches:
        code = requests.get(breach[1])
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        base_url = 'https://ago.vermont.gov'
        pdf_extension = s('a',{'class':"pdfemb-viewer"})[0].get('href')
        total_url = base_url + pdf_extension
        
        response = requests.get(total_url)
        my_raw_data = response.content

        with open("new_pdf.pdf", 'wb') as my_data:
            my_data.write(my_raw_data)
        my_data.close()
        
        file = textract.process('new_pdf.pdf', method='pdfminer')
        
        vermont_dict[year[-4:]][breach[0]] = file
        os.remove("new_pdf.pdf")
print("--- %s seconds ---" % (time.time() - start_time))        
print (vermont_dict)