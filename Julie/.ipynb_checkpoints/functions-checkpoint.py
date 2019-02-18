from bs4 import BeautifulSoup
import pandas as pd
import textract
import requests
import os

def basic_beautiful_soup(url):
    
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    return s
    
def download_parse_file(url):
    
    response = requests.get(url)
    my_raw_data = response.content

    with open("new_pdf.pdf", 'wb') as my_data:
        my_data.write(my_raw_data)
    my_data.close()
        
    return textract.process('new_pdf.pdf', method='pdfminer')

def update_Oregon(most_recent_breach):

    more_info_urls = []
    main_url = 'https://justice.oregon.gov/consumer/DataBreach/Home/'
    oregon = pd.read_html(main_url)[0]

    s = basic_beautiful_soup(main_url)
    
    for x in s('table', {'class':"webgrid-table", 'id':"grid"}):
        for item in x('a'):
            more_info_urls.append('https://justice.oregon.gov' + item.get('href'))
    
    breaches_info = []
    most_recent_breach = more_info_urls[0]
    
    for url in more_info_urls:
        while url != most_recent_breach:
            try:
                temp = pd.read_html(url)[0].set_index(0).to_dict()[1]
                breaches_info.append(temp)#more_info = pd.concat([more_info, temp])
            except:
                pass
    
    more_info = pd.DataFrame(breaches_info)

    more_info = more_info.drop(columns = ['Reported Date:', 'Date(s) of Breach:'])
    more_info.columns = ['Date(s) of Discovery of Breach', 'Notice Provided to Consumers' ,'Organization']

    df = pd.merge(oregon, more_info)
    
    return df, most_recent_breach