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
                for item in temp_dict:
                    breaches_info[item].append(temp_dict[item])

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
