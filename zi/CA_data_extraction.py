# In[5]:

import requests
from bs4 import BeautifulSoup


# # Scraping Main California Data Breach ASite

# In[2]:

response = requests.get('https://oag.ca.gov/privacy/databreach/list')


# In[7]:

c = response.content


# In[9]:

soup = BeautifulSoup(c, "lxml")


# # Identifying the table of breaches on the page and converting it to a CSV

# In[40]:

breach_table = soup.find('table')


# In[41]:

headers = [header.text for header in breach_table.find_all('th')]


# In[43]:

rows = []


# In[60]:

for row in breach_table.find_all('tr'):
    rows.append([val.text.encode('utf8') for val in row.find_all('td')])


# In[61]:

import csv


# In[62]:

with open('CA_Data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(row for row in rows if row)


# # Getting the Links to Sample Notice PDFS

# In[80]:

import re


# In[85]:

links = soup.tbody.find_all('a')

# In[129]:

from pathlib import Path


# Downloading all pdfs (if they exist)
# In[131]:

i = 0

for link in links:
    try:
        resp = requests.get(link.get('href'))
        c = resp.content
        soup = BeautifulSoup(c, "lxml")
        span = soup.find(class_="file")
        filename = Path('Data/CA/{}sample_notice.pdf'.format(i))
        url = span.a.get('href')
        response = requests.get(url)
        filename.write_bytes(response.content)
        new_file = 'last_attempt_url.txt'
        new_days = open(new_file, 'w')
        title = link.get('href')
        new_days.write(title)
        print(title)
        i += 1
    except:
        i += 1
        pass



