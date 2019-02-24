from bs4 import BeautifulSoup
import pandas as pd
import textract
import requests
import os
import csv
import re
from pathlib import Path


def basic_beautiful_soup(url):
    
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    return s
    
def download_parse_file(url):
    
    # Get the contents of the pdf file
    response = requests.get(url)
    my_raw_data = response.content
    # Write the contents into a temporary file
    with open("new_pdf.pdf", 'wb') as my_data:
        my_data.write(my_raw_data)
    my_data.close()
    
    # Try to convert the contents of the pdf to a string     
    try:
        file = textract.process('new_pdf.pdf', method='pdfminer')
    except:
        file = "Unreadable File"   

    # Delete the temporary file
    os.remove("new_pdf.pdf")

    # Return the string contents of the pdf
    return file


def update_Oregon(most_recent_breach):

    more_info_urls = []
    main_url = 'https://justice.oregon.gov/consumer/DataBreach/Home/'
    oregon = pd.read_html(main_url)[0]

    s = basic_beautiful_soup(main_url)
    
    for x in s('table', {'class':"webgrid-table", 'id':"grid"}):
        for item in x('a'):
            more_info_urls.append('https://justice.oregon.gov' + item.get('href'))

    breaches_info = {'Organization Name': [], 'Reported Date': [],
                    'Date(s) of Breach':[], 'Date(s) of Discovery of Breach': [],
                    'Notice Provided to Consumers':[]}
    
    
    for url in more_info_urls:
        if url != most_recent_breach:
            try:
                temp_dict = {}
                s2 = basic_beautiful_soup(url)
                l = []
                for x in s2('td'):
                    l.append(x.text.strip(':').strip('\r').strip('\n'))
                for item in l[::2]:
                    temp_dict[item] = l[l.index(item)+1]
                breaches_info['Organization Name'].append(temp_dict.get('Organization Name', ''))  
                breaches_info['Reported Date'].append(temp_dict.get('Reported Date', ''))
                breaches_info['Date(s) of Breach'].append(temp_dict.get('Date(s) of Breach', ''))
                breaches_info['Date(s) of Discovery of Breach'].append(temp_dict.get('Date(s) of Discovery of Breach', ''))
                breaches_info['Notice Provided to Consumers'].append(temp_dict.get('Notice Provided to Consumers', ''))
                
            except:
                pass
        #else:
        #    break 
    most_recent_breach = more_info_urls[0]
    more_info = pd.DataFrame(breaches_info)

    more_info = more_info.drop(columns = ['Reported Date', 'Date(s) of Breach'])
    more_info = more_info.rename(index=str, columns={"Organization Name": "Organization"})
    #more_info.columns = ['Date(s) of Discovery of Breach', 'Notice Provided to Consumers' ,'Organization']
    
    df = pd.merge(oregon, more_info)
    df = df.rename(index=str, columns={"Organization": "Name of Entity ", 'Notice Provided to Consumers': 'Date Notice Provided to Consumers'})
    df['State Reported'] = 'Oregon'
    return df, most_recent_breach


def update_Wisconsin(most_recent_breach):

    current_url = 'https://datcp.wi.gov/Pages/Programs_Services/DataBreaches.aspx'
    temp = pd.read_html(current_url)
    rows_list = []
    for breach in temp:
        row = {'Notice Provided to Consumers':breach.iloc[1][0],
               'Dates of Breach':breach.iloc[1][1],
               'Name of Entity':breach.iloc[1][2],
               'Data Stolen':breach.iloc[1][3],
               "Who's Affected":breach.iloc[3][0],
               'Details':breach.iloc[3][1]}
        rows_list.append(row)
    wisconsin_now = pd.DataFrame(rows_list)

    pre_current_year_url = 'https://datcp.wi.gov/Pages/Programs_Services/DataBreachArchive.aspx'
    temp = pd.read_html(pre_current_year_url)
    rows_list = []
    for breach in temp:
        row = {'Notice Provided to Consumers':breach.iloc[1][0],
               'Dates of Breach':breach.iloc[1][1],
               'Name of Entity':breach.iloc[1][2],
               'Data Stolen':breach.iloc[1][3], 
               "Who's Affected":breach.iloc[3][0],
               'Details':breach.iloc[3][1]}
        rows_list.append(row)
    wisconsin_archive = pd.DataFrame(rows_list)

    wisconsin = pd.concat([wisconsin_now, wisconsin_archive], ignore_index = True)
    wisconsin['State Reported'] = 'Wisconsin'
    return (wisconsin, 'xyz')

def update_Vermont(most_recent_breach):
    url = 'https://ago.vermont.gov/archived-security-breaches/'
    base_url = 'https://ago.vermont.gov'

    s = basic_beautiful_soup(url)

    year_urls= []
    
    for x in s('li', {'class':"awDatesLI"}):
        for item in x('a'):
            year_urls.append(item.get('href'))

    vermont_dict = {'Name of Entity':[],
                    'PDF text (ALL)':[],
                    'Link to PDF':[]}
    for year in year_urls:
        
        breaches = []
        s_year = basic_beautiful_soup(year)

        for x in s_year('div', {'id':"postWrapper"}):
            for item in x('a'):
                breaches.append((item('h3',{'class':'awyca_subheader'})[0].text,item.get('href')))

        for breach in breaches:
            s_breach = basic_beautiful_soup(breach[1])
            pdf_extension = s_breach('a',{'class':"pdfemb-viewer"})[0].get('href')
            total_url = base_url + pdf_extension
            file = download_parse_file(total_url)
            vermont_dict['Name of Entity'].append(breach[0].replace('Notice of Data Breach to Consumers','').replace('SBN to Consumers',''))
            vermont_dict['PDF text (ALL)'].append(file)
            vermont_dict['Link to PDF'].append(breach[1])


    vermont = pd.DataFrame(vermont_dict)
    vermont['State Reported'] = 'Vermont'


    return vermont, 'xyz'

def update_Washington(most_recent_breach):
    url = 'http://www.atg.wa.gov/data-breach-notifications'

    washington = pd.read_html(url, skiprows = 2)[1]
    
    washington = washington.rename(index = str, columns = {0:'Reported Date', 1:'Name of Entity', 2:'Dates of Breach'})
    washington = washington.dropna()
    washington['State Reported'] = 'Washington'

    s = basic_beautiful_soup(url)
    pdf_links = []
    for breach in s('td')[5:]:
        if breach('a'):
            pdf_links.append(breach('a')[0].get('href'))

    washington['Link to PDF'] = pdf_links
    washington['PDF text (ALL)'] = washington['Link to PDF'].apply(download_parse_file)

    #print (washington.head())

    return washington, 'xyz'

def update_California(most_recent_breach):

    url = 'https://oag.ca.gov/privacy/databreach/list'
    
    s = basic_beautiful_soup(url)
    breach_table = s.find('table')
    headers = [header.text for header in breach_table.find_all('th')]
    
    rows = []
    for row in breach_table.find_all('tr'):
        rows.append([val.text.encode('utf8') for val in row.find_all('td')])

    california = pd.DataFrame(columns = headers, data =rows[1:])
    california = california.rename(index=str, columns={"Organization Name": "Name of Entity", 'Date(s) of Breach': 'Dates of Breach'})


    links = s.tbody.find_all('a')

    files = []
    for link in links:
        try:
            resp = requests.get(link.get('href'))
            c = resp.content
            soup = BeautifulSoup(c, "lxml")
            span = soup.find(class_="file")
            url = span.a.get('href')
            files.append(download_parse_file(url))
        except:
            files.append('')
    california['PDF text (ALL)'] = files
    california['State Reported'] = 'California'


    return california, "xyz"

def update_Indiana(most_recent_breach):
    pass

def update_Iowa(most_recent_breach):
    pass

def update_Delaware(most_recent_breach):
    pass

def update_NewHampshire(most_recent_breach):
    pass

def update_NewJersey(most_recent_breach):
    pass

def update_USDeptHealth(most_recent_breach):
    url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
    tables = pd.read_html(url)
    USDH = tables[1]
    USDH.drop(['Expand All'], axis=1)
    USDH = USDH.rename(index=str, columns={"Name of Covered Entity": "Name of Entity", 'State': 'State Reported', 
        'Covered Entity': "Entity Type", 'Breach Submission Date': 'Reported Date'})
    states = { 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming' }
    USDH['State Reported'] = USDH['State Reported'].apply(lambda x: states[x])
    return USDH, 'xyz'

def update_Maine(most_recent_breach):
    pass

def update_Maryland(most_recent_breach):
    pass

def update_Massachusetts(most_recent_breach):
    pass

def update_Montana(most_recent_breach):
    pass