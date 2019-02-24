import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh

url = 'https://www.cyber.nj.gov/data-breach-alerts'
res = requests.get(url)
links = list()
soup = BeautifulSoup(res.content, 'html.parser')
for a in soup.findAll("a", {"class": "BlogList-item-title"},  href=True):
	links.append(a['href'])


print(links)