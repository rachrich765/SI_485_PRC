#9.667921781539917 seconds

import time
start_time = time.time()

import pandas as pd
import requests
import textract
import os
from bs4 import BeautifulSoup

current_url = 'https://datcp.wi.gov/Pages/Programs_Services/DataBreaches.aspx'


temp = pd.read_html(current_url)
rows_list = []
for breach in temp:
    row = {'Date Public Notified':breach.iloc[1][0],
           'Date of Breach':breach.iloc[1][1],
           'Company':breach.iloc[1][2],
           'Data Stolen':breach.iloc[1][3], 
           "Who's Affected":breach.iloc[3][0],
           'Details':breach.iloc[3][1]}
    rows_list.append(row)
wisconsin_now = pd.DataFrame(rows_list)

pre_current_year_url = 'https://datcp.wi.gov/Pages/Programs_Services/DataBreachArchive.aspx'
temp = pd.read_html(pre_current_year_url)
rows_list = []
for breach in temp:
    row = {'Date Public Notified':breach.iloc[1][0],
           'Date of Breach':breach.iloc[1][1],
           'Company':breach.iloc[1][2],
           'Data Stolen':breach.iloc[1][3], 
           "Who's Affected":breach.iloc[3][0],
           'Details':breach.iloc[3][1]}
    rows_list.append(row)
wisconsin_archive = pd.DataFrame(rows_list)

wisconsin = pd.concat([wisconsin_now, wisconsin_archive], ignore_index = True)
print("--- %s seconds ---" % (time.time() - start_time))  
print(wisconsin.head())