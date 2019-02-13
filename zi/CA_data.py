import requests
from bs4 import BeautifulSoup

response = requests.get('https://oag.ca.gov/privacy/databreach/list')
c = response.content
soup = BeautifulSoup(c, "lxml")

breach_table = soup.find('table')
headers = [header.text for header in breach_table.find_all('th')]
rows = []
