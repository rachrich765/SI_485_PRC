import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh
import csv



url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
#find table on page using pandas
tables = pd.read_html(url)
#get table with desired data
data_USDHHSOCR = tables[1]
#write pandas table to CSV file
data_USDHHSOCR.to_csv(path_or_buf='USDHHSOCR_data.csv')
print("--- %s seconds ---" % (time.time() - start_time))  