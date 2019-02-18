# 156.54826593399048 seconds 
# about 2.5 min

import time
start_time = time.time()

import pandas as pd
import requests
import textract
import os
from bs4 import BeautifulSoup

main_url = 'https://justice.oregon.gov/consumer/DataBreach/Home/'
oregon = pd.read_html(main_url)[0]

code = requests.get(main_url)
plain = code.text
s = BeautifulSoup(plain, "html.parser")

more_info_urls = []
for x in s('table', {'class':"webgrid-table", 'id':"grid"}):
    for item in x('a'):
        more_info_urls.append('https://justice.oregon.gov' + item.get('href'))
breaches_info = []
for url in more_info_urls:
    try:
        temp = pd.read_html(url)[0].set_index(0).to_dict()[1]
        breaches_info.append(temp)#more_info = pd.concat([more_info, temp])
    except:
        pass
more_info = pd.DataFrame(breaches_info)

more_info = more_info.drop(columns = ['Reported Date:', 'Date(s) of Breach:'])
more_info.columns = ['Date(s) of Discovery of Breach', 'Notice Provided to Consumers' ,'Organization']

df = pd.merge(oregon, more_info)
print("--- %s seconds ---" % (time.time() - start_time))       
print (df.head())