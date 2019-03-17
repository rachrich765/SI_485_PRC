import time
start_time = time.time()

import pandas as pd
import requests
from bs4 import BeautifulSoup
import lxml.html as lh
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')

tables1 = list()
driver = webdriver.Chrome()
driver.get(url)
columns = ['Expand All', 'Name of Covered Entity', 'State', 'Covered Entity Type',
       'Individuals Affected', 'Breach Submission Date', 'Type of Breach',
       'Location of Breached Information']
usdh = pd.DataFrame(columns = columns)

python_button = driver.find_elements_by_xpath("//a[@class='ui-paginator-page ui-state-default ui-corner-all']")
buttons = len(python_button)

y = driver.page_source
tables = pd.read_html(y, header=0)
data_USDHHSOCR = tables[1]
usdh = usdh.append(data_USDHHSOCR, ignore_index = True)
for i in range(buttons):
	python_button = driver.find_elements_by_xpath("//a[@class='ui-paginator-page ui-state-default ui-corner-all']")
	x = python_button[i]
	x.click()
	time.sleep(5)
	y = driver.page_source
	tables = pd.read_html(y, header=0)
	data_USDHHSOCR = tables[1]

	usdh = usdh.append(data_USDHHSOCR, ignore_index = True)
driver.quit()
usdh = usdh.drop(['Expand All'], axis=1)
usdh = usdh.rename(index=str, columns={"Name of Covered Entity": "Name of Entity", 'State': 'State Reported', 
	'Covered Entity Type': "Entity Type", 'Breach Submission Date': 'Reported Date'})
states = { 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming' }
usdh['State Reported'] = usdh['State Reported'].apply(lambda x: states[x])

usdh.to_csv('USDeptHealth.csv')

print (len(usdh))
print(usdh.head())
end_time = time.time()
minutes = (end_time - start_time)/60
print("minutes:", minutes)