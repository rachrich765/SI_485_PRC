from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import numpy as np
import textract
import requests
import datetime
import json
import os
import csv
import re


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
    
    df = pd.merge(oregon, more_info, how = 'left', on = 'Organization')
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
    print (len(california))
    files = []
    x = 0
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
        x += 1
        print (x)
    california['PDF text (ALL)'] = files
    california['State Reported'] = 'California'


    return california, "xyz"

def update_Indiana(most_recent_breach):
    
    url = 'https://www.in.gov/attorneygeneral/2874.htm'
    url_front = 'https://www.in.gov/'
    #columns = ['Name of Entity','Date Notice Provided to Consumers','Dates of Breach','Number of IN Residents Affected','Number of Consumers Affected Nationwide','Disposition','Status']
    columns = ['Name of Entity', 'Date Notice Provided to Consumers',
       'Dates of Breach', 'Number of IN Residents Affected',
       'Number of Consumers Affected Nationwide', 'Status']
    indiana = pd.DataFrame(columns=columns)

    s = basic_beautiful_soup(url)
    breach_links = s.find('p', relativehref='[ioID]8026AD70E4164E4E9F9FE8FA5553BA5C/2016_04_01_ITU_Breach(1).pdf')('a')
    full_breach_links = []
    for link in breach_links:
        full_breach_links.append(url_front + link.get('href'))

    for url in full_breach_links[2:]:
        if '.pdf' in url:
            response = requests.get(url)
            my_raw_data = response.content
            with open("new_pdf.pdf", 'wb') as my_data:
                my_data.write(my_raw_data)
                my_data.close()
            fileData = ("new_pdf.pdf", open("new_pdf.pdf", 'rb')) #"rb" stands for "read bytes"
            files = {'f': fileData} 
            apiKey = "6wb10txsz9f9" 
            fileExt = "csv" #format/file extension of final document
            postUrl = "https://pdftables.com/api?key={0}&format={1}".format(apiKey, fileExt)
            response = requests.post(postUrl, files=files)
            response.raise_for_status() # ensure we notice bad responses
            downloadDir = "example.csv" #directory where you want your file downloaded to 

            with open(downloadDir, "wb") as f:
                f.write(response.content) #write data to csv
            temp = pd.read_csv(downloadDir)
            if len(temp.columns) == 6:
                temp.columns = ['Name of Entity','Date Notice Provided to Consumers','Dates of Breach','Number of IN Residents Affected','Number of Consumers Affected Nationwide','Disposition']
            else:
                temp.columns = ['Name of Entity','Date Notice Provided to Consumers','Dates of Breach','Number of IN Residents Affected','Disposition']

            temp = temp.drop(temp.index[0])
            indiana = indiana.append(temp, ignore_index = True)

            os.remove("new_pdf.pdf")
            os.remove("example.csv")
        else:
            resp = requests.get(url)
            output = open('in_one_year.xls', 'wb')
            output.write(resp.content)
            output.close()

            temp = pd.read_excel('in_one_year.xls') 
            os.remove('in_one_year.xls')
            #print (temp.columns)
            if 'Respondent' in temp.columns:
                #print('x')
                temp_new = temp.rename(index=str, columns={'Respondent':'Name of Entity',  
                    'Notification Sent':'Date Notice Provided to Consumers',
                    'Breach Occurred':'Dates of Breach',
                    'IN Affected':'Number of IN Residents Affected',
                    'Total Affected':'Number of Consumers Affected Nationwide'})
                
                indiana = indiana.append(temp_new, ignore_index = True)
                #print (temp.columns)
            elif "Name of Company or Organization " in temp.columns:
                #print('y')
                temp_new = temp.rename(index=str, columns={'Name of Company or Organization ':'Name of Entity', 
                    'Date of Notification ':'Date Notice Provided to Consumers', 
                    'Date of Breach ':'Dates of Breach',
                    'Number of Indiana Residents Affected ':'Number of IN Residents Affected',
                    'Number of Consumers Affected Nationwide ':'Number of Consumers Affected Nationwide',
                    'Disposition':'Status'})
               
                indiana = indiana.append(temp_new, ignore_index = True)#in temp.columns:
    
    indiana['Number of Consumers Affected Nationwide'] = indiana['Number of Consumers Affected Nationwide'].apply(lambda x: 'Unknown' if pd.isnull(x) else str(x))
    indiana['Number of IN Residents Affected'] = indiana['Number of IN Residents Affected'].apply(lambda x: 'Unknown' if pd.isnull(x) else str(x))
    indiana['Individuals Affected'] = indiana['Number of Consumers Affected Nationwide']+' ('+ indiana['Number of IN Residents Affected'] +' in Indiana)'
    indiana = indiana.drop(columns = ['Number of Consumers Affected Nationwide','Number of IN Residents Affected','Status', 'Unnamed: 1'])
    
    return indiana, 'xyz'

def update_Iowa(most_recent_breach):
    base_url = 'https://www.iowaattorneygeneral.gov'
    first_year = 2011
    last_year = datetime.datetime.today().year
    columns = ['Name of Entity', 'Reported Date']
    iowa = pd.DataFrame(columns=columns)
    for year in range(first_year,last_year+1):
        if (year != 2017 and year != 2019):
            url = 'https://www.iowaattorneygeneral.gov/for-consumers/security-breach-notifications/{}-security-breach-notifications/'.format(year)
        else:
            url = 'https://www.iowaattorneygeneral.gov/for-consumers/security-breach-notifications/{}'.format(year)
        temp = pd.read_html(url)[0]
        temp = temp.rename(columns=temp.iloc[0])
        temp = temp.drop(temp.index[0])
        temp = temp.dropna(how = 'all')
        s = basic_beautiful_soup(url)
        links = s.find('table')('a')
        pdfs = []
        links_pdfs = []
        for item in links:
            if item.get('href'):
                url = base_url + item.get('href')
                links_pdfs.append(url)
                pdfs.append(download_parse_file(url))
            else:
                pdfs.append('')
 
        #breach_table = s.find('table')
        #headers = [header.text for header in breach_table.find_all('h4')]
 
        temp['PDF text (ALL)'] = pdfs
        temp['Link to PDF'] = links_pdfs
        

        #print (temp.columns)
        if 'YEAR REPORTED' in temp.columns:
            temp['YEAR REPORTED'] = year
            temp = temp.rename(columns = {'YEAR REPORTED':'Reported Date','ORGANIZATION NAME':'Name of Entity'})
        else: 
            temp = temp.rename(columns = {'DATE REPORTED':'Reported Date','ORGANIZATION NAME':'Name of Entity'})
        iowa = iowa.append(temp,ignore_index=True)
        iowa['State Reported'] = 'Iowa'
    return iowa, 'xyz'

def update_Delaware(most_recent_breach):

    url = 'https://attorneygeneral.delaware.gov/fraud/cpu/securitybreachnotification/database/'
    delaware = pd.read_html(url)[0]
    s = basic_beautiful_soup(url)

    links = s.tbody.find_all('a')

    #i = 0
    pdfs = []
    for link in links:
        try:
            #print (link.get('href'))
            pdfs.append(download_parse_file(link.get('href')))
            #i+=1
    
        except:
            #i+=1
            pass
    
    delaware = delaware.rename(index=str, columns={'Organization Name': 'Name of Entity', 'Date(s) of Breach':'Dates of Breach',
        'Number of Potentially Affected Delaware Residents': 'Individuals Affected'})
    delaware = delaware.drop(columns = ["Sample of Notice"])
    
    delaware['Individuals Affected'] = delaware['Individuals Affected'].apply(lambda x: str(x)+'(in Delaware)')
    delaware['PDF text (ALL)'] = pdfs
    delaware['State Reported'] = 'Delaware'


    return delaware, 'xyz'


def update_NewHampshire(most_recent_breach):
    pass

def update_NewJersey(most_recent_breach):
    pass

def update_USDeptHealth(most_recent_breach):
    print ('INCOMPLETE')
    url = 'https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf'
    tables = pd.read_html(url)
    USDH = tables[1]
    USDH.drop(['Expand All'], axis=1)
    USDH = USDH.rename(index=str, columns={"Name of Covered Entity": "Name of Entity", 'State': 'State Reported', 
        'Covered Entity': "Entity Type", 'Breach Submission Date': 'Reported Date'})
    states = { 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands', 'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming' }
    USDH['State Reported'] = USDH['State Reported'].apply(lambda x: states[x])
    print (len(USDH))
    return USDH, 'xyz'

def update_Maine(most_recent_breach):
    url = 'https://www.maine.gov/ag/consumer/identity_theft/' #URL of Main webpage
    s = basic_beautiful_soup(url)

    year_url = [] #creates URL string
    for x in s('ul', {'class':"plain"}): #iterates through the neccisary HTML to get needed href
        for item in x('a'):
#       print(item)   
            if item.get('href') != 'https://appengine.egov.com/apps/nics/Maine/AGReportingForm':
                year_url.append(item.get('href')) #retrieves and asisngs needed content (str) to year_url varialbe
    
    core_year_url = 'https://www.maine.gov/ag'
    current_breaches = core_year_url + year_url[0][5:]
    archived_breaches = core_year_url + year_url[1][5:]
    
    
    resp = requests.get(archived_breaches)
    output = open('Maine.xls', 'wb')
    output.write(resp.content)
    output.close()

    df = pd.read_excel('Maine.xls') 
    os.remove("Maine.xls")

    headers = df.iloc[0] #takes first row (needed hearders)
    maine_arch = pd.DataFrame(df.values[1:], columns=headers) #creates new pd data frame with the proper headers and fills data
    maine_arch = maine_arch.dropna(how = 'all')
    maine_arch = maine_arch.drop(columns = ['Company Contact Information','Attorney                   (If Represented)'])

    maine_arch = maine_arch.rename(index=str, columns={"Company Whose      Data Was Breached": "Name of Entity",
        'Date of Breach':'Dates of Breach',
        'Date of Notification':'Date Notice Provided to Consumers', 'Type of Information':'Data Stolen', 
        'Number of Maine Residents Affected':'Individuals Affected'})

    maine_arch['Individuals Affected'] = maine_arch['Individuals Affected'].apply(lambda x: str(x) + '(in Maine')

    resp = requests.get(current_breaches)
    output = open('Maine.xls', 'wb')
    output.write(resp.content)
    output.close()

    maine_current = pd.read_excel('Maine.xls') 
    os.remove("Maine.xls")
    #print (maine_current.columns)
    maine_current['Entity Address'] = maine_current['01_03_02_Street Address'] + maine_current['01_03_03_City']+ maine_current['01_03_04_State'] + maine_current['01_03_05_Zip Code']
    maine_current['01_04_01_Educational'] = maine_current['01_04_01_Educational'].apply(lambda x: 'Educational ' if x == True else '')
    maine_current['01_04_02_Financial Services (if reporting to the Department of Professional and Financial Services, this form is not required. 10 M.R.S.A. §1348(5))'] = maine_current['01_04_02_Financial Services (if reporting to the Department of Professional and Financial Services, this form is not required. 10 M.R.S.A. §1348(5))'].apply(lambda x: 'Financial Services ' if x == True else '')
    maine_current['01_04_03_Governmental Entity in Maine'] = maine_current['01_04_03_Governmental Entity in Maine'].apply(lambda x: 'Governmental Entity in Maine ' if x == True else '')
    maine_current['01_04_04_Other Governmental Entity'] = maine_current['01_04_04_Other Governmental Entity'].apply(lambda x: 'Other Governmental Entity ' if x == True else '')
    maine_current['01_04_05_Health Care'] = maine_current['01_04_05_Health Care'].apply(lambda x: 'Health Care ' if x == True else '')
    maine_current['01_04_06_Other Commercial'] = maine_current['01_04_06_Other Commercial'].apply(lambda x: 'Other Commercial ' if x == True else '')
    maine_current['01_04_07_Not-for-Profit'] = maine_current['01_04_07_Not-for-Profit'].apply(lambda x: 'Not-for-Profit ' if x == True else '')
    maine_current['01_04_08_POS Vendor'] = maine_current['01_04_08_POS Vendor'].apply(lambda x: 'POS Vendor ' if x == True else '')
    
    maine_current['Entity Type'] = maine_current['01_04_01_Educational'] + maine_current['01_04_02_Financial Services (if reporting to the Department of Professional and Financial Services, this form is not required. 10 M.R.S.A. §1348(5))'] + maine_current['01_04_03_Governmental Entity in Maine'] + maine_current['01_04_05_Health Care'] + maine_current['01_04_06_Other Commercial'] + maine_current['01_04_07_Not-for-Profit'] + maine_current['01_04_08_POS Vendor']
    
    maine_current['Individuals Affected'] = maine_current['02_01_01_Total number of persons affected (including Maine residents)'] + '(' + maine_current['02_01_02_Total number of Maine residents affected'] + ' in Maine)'

    maine_current['02_02_01_Loss or theft of device or media (e.g., computer, laptop, external hard drive, thumb drive, CD, tape)'] = maine_current['02_02_01_Loss or theft of device or media (e.g., computer, laptop, external hard drive, thumb drive, CD, tape)'].apply(lambda x: 'Loss or theft of device or media (e.g., computer, laptop, external hard drive, thumb drive, CD, tape) ' if x == True else '')
    maine_current['02_02_02_Internal system breach'] = maine_current['02_02_02_Internal system breach'].apply(lambda x: 'Internal system breach ' if x == True else '') 
    maine_current['02_02_03_Insider wrongdoing'] = maine_current['02_02_03_Insider wrongdoing'].apply(lambda x: 'Insider wrongdoing' if x == True else '')
    maine_current['02_02_04_External system breach (e.g., hacking)'] = maine_current['02_02_04_External system breach (e.g., hacking)'].apply(lambda x: 'External system breach (e.g., hacking)' if x == True else '')
    maine_current['02_02_05_Inadvertent disclosure'] =  maine_current['02_02_05_Inadvertent disclosure'].apply(lambda x: 'Inadvertent disclosure' if x == True else '')
    #maine_current['02_02_06_Other'] = maine_current['02_02_06_Other']
    maine_current['02_02_07_If other, specify'] = maine_current['02_02_07_If other, specify'].apply(lambda x: '' if x == None else x)

    maine_current['Cause of Breach'] = maine_current['02_02_01_Loss or theft of device or media (e.g., computer, laptop, external hard drive, thumb drive, CD, tape)']+ maine_current['02_02_02_Internal system breach'] + maine_current['02_02_03_Insider wrongdoing'] + maine_current['02_02_04_External system breach (e.g., hacking)']+maine_current['02_02_04_External system breach (e.g., hacking)'] + maine_current['02_02_05_Inadvertent disclosure'] + maine_current['02_02_07_If other, specify']
    
    maine_current['02_03_01_Social Security Number'] = maine_current['02_03_01_Social Security Number'].apply(lambda x: 'Social Security Number ' if x == True else '')
    maine_current["02_03_02_Driver's license number or non-driver identification card number"] = maine_current["02_03_02_Driver's license number or non-driver identification card number"].apply(lambda x: "Driver's license number or non-driver identification card number " if x == True else '')
    maine_current['02_03_03_Financial account number or credit or debit card number, in combination with the security code, access code,  password, or PIN for the account'] = maine_current['02_03_03_Financial account number or credit or debit card number, in combination with the security code, access code,  password, or PIN for the account'].apply(lambda x: 'Financial account number or credit or debit card number, in combination with the security code, access code,  password, or PIN for the account ' if x == True else '')

    maine_current['Data Stolen'] = maine_current['02_03_01_Social Security Number'] + maine_current["02_03_02_Driver's license number or non-driver identification card number"]+maine_current['02_03_03_Financial account number or credit or debit card number, in combination with the security code, access code,  password, or PIN for the account']


    maine_current = maine_current.drop(columns = ['Start Date','01_03_02_Street Address','01_03_03_City', '01_03_04_State', '01_03_05_Zip Code',
       '01_04_01_Educational','01_04_02_Financial Services (if reporting to the Department of Professional and Financial Services, this form is not required. 10 M.R.S.A. §1348(5))',
        '01_04_03_Governmental Entity in Maine','01_04_04_Other Governmental Entity','01_04_05_Health Care','01_04_06_Other Commercial','01_04_07_Not-for-Profit','01_04_08_POS Vendor',
        '01_05_01_Name', '01_05_02_Title',
        '01_05_03_Firm name (if different than entity name)',
        '01_05_04_Telephone Number', '01_05_05_Email Address',
        '01_05_06_Relationship to entity whose information was compromised',
        '02_01_01_Total number of persons affected (including Maine residents)',
        '02_01_02_Total number of Maine residents affected',
        '02_01_03_If the number of Maine residents exceeds 1,000, have the consumer reporting agencies been notified?','02_02_01_Loss or theft of device or media (e.g., computer, laptop, external hard drive, thumb drive, CD, tape)',
        '02_02_02_Internal system breach', '02_02_03_Insider wrongdoing',
        '02_02_04_External system breach (e.g., hacking)',
        '02_02_05_Inadvertent disclosure', '02_02_06_Other',
        '02_02_07_If other, specify','03_01_01_Written', '03_01_02_Electronic', '03_01_03_Telephone',
        '03_01_04_Substitute notice','03_01_06_Attach a copy of the template of the notice to affected Maine residents',
        '03_02_01_Were identify theft protection services offered?',
        '03_02_02_If yes, for what duration?',
        '03_02_03_If yes, by what provider?',
        '03_02_04_If yes, provide a brief description of the service.',
        '02_03_01_Social Security Number',
       "02_03_02_Driver's license number or non-driver identification card number",
       '02_03_03_Financial account number or credit or debit card number, in combination with the security code, access code,  password, or PIN for the account',
       '03_01_07_List dates of any previous (within 12 months) breach notifications'])

    maine_current = maine_current.rename(index=str, columns={'01_03_01_Entity Name':'Name of Entity',
        '02_01_04_Date(s) Breach Occurred':'Dates of Breach', '02_01_05_Date Breach Discovered':'Date(s) of Discovery of Breach', 
        '03_01_05_Date(s) of consumer notification':'Date Notice Provided to Consumers'})


    #print ('NEED TO HANDLE MAINE CURRENT AND merge')
    #print (maine_current.head())
    maine = pd.concat([maine_current, maine_arch], ignore_index = True)
    maine['State Reported'] = 'Maine'
    
    return maine, 'xyz'

def update_Maryland(most_recent_breach):
    murl = 'http://www.marylandattorneygeneral.gov/Pages/IdentityTheft/breachnotices.aspx'
    s = basic_beautiful_soup(murl)
    years = range(2015,datetime.datetime.now().year)
    counts = {}
    for x in years:
        soup = str(s('tbody',{'groupstring':'%3B%23{}%3B%23'.format(str(x))}))
        counts[x] = int(re.findall(r'\(([0-9]*?)\)',str(soup))[0])
    print (counts)
    year = 2016#2015
    string = "&p_Year=" +str(year) 
    base_url = "http://www.marylandattorneygeneral.gov/_layouts/15/inplview.aspx?List=%7B04EBF6F4-B351-492F-B96D-167E2DE39C85%7D&View=%7BAC628F51-0774-4B71-A77E-77D6B9909F7E%7D&ViewCount=4&IsXslView=TRUE&IsCSR=TRUE&ListViewPageUrl=http%3A%2F%2Fwww.marylandattorneygeneral.gov%2FPages%2FIdentityTheft%2Fbreachnotices.aspx&p_Date_x0020_Received=20161219%2005%3a00%3a00&p_ID=4199&GroupString=%3b%232016%3b%23&IsGroupRender=TRUE&WebPartID={AC628F51-0774-4B71-A77E-77D6B9909F7E}"
    url = base_url + string

    rows = []
    page_start = 1
    page_start = 1
    while year < 2019:
        string = "&p_Year=" +str(year) 
        base_url = "http://www.marylandattorneygeneral.gov/_layouts/15/inplview.aspx?List=%7B04EBF6F4-B351-492F-B96D-167E2DE39C85%7D&View=%7BAC628F51-0774-4B71-A77E-77D6B9909F7E%7D&ViewCount=4&IsXslView=TRUE&IsCSR=TRUE&ListViewPageUrl=http%3A%2F%2Fwww.marylandattorneygeneral.gov%2FPages%2FIdentityTheft%2Fbreachnotices.aspx&p_Date_x0020_Received={}1219%2005%3a00%3a00&p_ID=4199&GroupString=%3b%23{}%3b%23&IsGroupRender=TRUE&WebPartID={AC628F51-0774-4B71-A77E-77D6B9909F7E}".format(year,year)
        url = base_url + string
        #stop =  counts[year]//30 + 1
        #print(stop)
        if counts[year] > page_start:
            result = requests.post(url, headers={'referer': "http://www.marylandattorneygeneral.gov/Pages/IdentityTheft/breachnotices.aspx"})
#         print(result.text)
            data = json.loads(result.text)
            for x in data['Row']:
                rows.append({
                    'case_title': x['Case_x0020_Title'],
                    'case_number': x['FileLeafRef.Name'],
                    'date_received': x['Date_x0020_Received'],
                    'how_breach_occurred': x['How_x0020_Breach_x0020_Occurred'],
                    'no_of_md_residents': x['No_x0020_of_x0020_MD_x0020_Residents']
                })
            page_start = page_start + 30
            #year += 1
            url = base_url + string + "&PageFirstRow={}".format(page_start)
            print(len(rows))
        else:
            year += 1
#         print("TEST BREAK")
            #break
    print(len(json_normalize(rows)))
    print(type(json_normalize(rows)))
    print(json_normalize(rows).head())
    maryland = json_normalize(rows)
    maryland.to_csv('test_maryland.csv')
    return maryland, 'xyz'

def update_Massachusetts(most_recent_breach):
    pass

def update_Montana(most_recent_breach):
    pass