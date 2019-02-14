import time
start_time = time.time()

import pandas as pd
import requests
import textract
from bs4 import BeautifulSoup
import lxml.html as lh



url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
tables = pd.read_html(url)
data_USDHHSOCR = tables[1]
print("--- %s seconds ---" % (time.time() - start_time))  
print(data_USDHHSOCR.head())