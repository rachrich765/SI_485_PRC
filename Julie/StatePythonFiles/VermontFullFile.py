# Reference: runtime for entire data breach history of vermont: 472.70189118385315 seconds (just under 8 min)

# Import necessary packages
import requests
import textract
import os
from bs4 import BeautifulSoup

# Use beautiful soup to parse the website where Vermont posts data about their data breaches.
url = 'https://ago.vermont.gov/archived-security-breaches/'
code = requests.get(url)
plain = code.text
s = BeautifulSoup(plain, "html.parser")

# Extract the urls for each year's data breach chronology.
year_urls= []
for x in s('li', {'class':"awDatesLI"}):
    for item in x('a'):
        year_urls.append(item.get('href'))

# Initialize dictionary to store all vermont data
vermont_dict = {}

# For each year, use beautiful soup to parse the page with that year's data breach chronology
for year in year_urls:
    vermont_dict[year[-4:]] = {}
    breaches = []
    code = requests.get(year)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")

# Extract the link for each breach.
    for x in s('div', {'id':"postWrapper"}):
        for item in x('a'):
            breaches.append((item('h3',{'class':'awyca_subheader'})[0].text,item.get('href')))

# For each breach link, extract the link for each breach to the pdf where the letter to consumers (from company) is stored.
    for breach in breaches:
        code = requests.get(breach[1])
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        base_url = 'https://ago.vermont.gov'
        pdf_extension = s('a',{'class':"pdfemb-viewer"})[0].get('href')
        total_url = base_url + pdf_extension
        
# Download the pdf and process it with textract to get the text from the pdf
        response = requests.get(total_url)
        my_raw_data = response.content

        with open("new_pdf.pdf", 'wb') as my_data:
            my_data.write(my_raw_data)
        my_data.close()
        
        file = textract.process('new_pdf.pdf', method='pdfminer')

# Add the text to the vermont dictionary and remove the downloaded file
        vermont_dict[year[-4:]][breach[0]] = file
        os.remove("new_pdf.pdf")

# NOTE: we are still developing the code / method for getting data points from each pdf file.
# That code will be appended to the vermont data extraction process. 
# Then, the dictionary will be converted to a pandas dataframe and merged with other states. 

