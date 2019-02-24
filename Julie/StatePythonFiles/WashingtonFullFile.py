#476.3654987812042 seconds
#just under 8 min

import pandas as pd
import requests
import textract
import os
from bs4 import BeautifulSoup
import time
start_time = time.time()

washington = pd.read_html("http://www.atg.wa.gov/data-breach-notifications'", skiprows = 2)[1]

washington.columns = ['Reported Date', 'Organization Name', 'Date of Breach']
washington = washington.dropna()

url = 'http://www.atg.wa.gov/data-breach-notifications'
code = requests.get(url)
plain = code.text
s = BeautifulSoup(plain, "html.parser")
y = []
for x in s('td')[5:]:
    if x('a'):
        y.append(x('a')[0].get('href'))

washington['PDF link'] = y


def get_text(pdf_link):
    
    total_url = pdf_link
        
    response = requests.get(total_url)
    my_raw_data = response.content

    with open("new_pdf.pdf", 'wb') as my_data:
        my_data.write(my_raw_data)
    my_data.close()
        
    try:
    	file = textract.process('new_pdf.pdf', method='pdfminer')
    except:
    	file = "Unreadable File"    
    os.remove("new_pdf.pdf")

    return file

washington['PDF text'] = washington['PDF link'].apply(get_text)

print("--- %s seconds ---" % (time.time() - start_time))    
print (washington.head(5))