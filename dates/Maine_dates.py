from datetime import datetime
import pandas as pd
import csv
import arrow
import re
from datetime import date
import dateutil.parser

new_M_dates = list()
new_M_dates_end = list()
def clean_Maine_dates(Maine_data):
    yy = Maine_data
    for y in yy['Dates of Breach']:
        y = str(y)
        if y.count('-') >= 1 and y.count('/') == 0:
            try: 
                d = datetime.strptime(y, "%d-%b-%y")
                new_M_dates.append(d)
            except: 
                new_M_dates.append(y)

        elif y.count('/') > 0 and y.count('/') <= 2:
            try:
                d = datetime.strptime(y, "%m/%d/%Y")
                new_M_dates.append(d)
            except:
                new_M_dates.append(y)
        
        elif ',' in y:
            try: 
                d = datetime.strptime(x, "%B %d, %Y")
                new_M_dates.append(y)
            except: 
                new_M_dates.append(y)
        elif y.lower() == 'unknown' or y =='?' or y.lower()=='not given'or y.lower()=='recently' or y.lower()=='not stated' or y.lower()=='see exhibit 1':
            new_M_dates.append('')
        else:
            new_M_dates.append(y)
    yy['Start Date of Breach'] = new_M_dates
    yy.to_csv('testMaine.csv')
    return yy

# replace this with Maine data
Maine_dates = pd.read_csv("C:/Users/atrm1/Downloads/Maine_dates.csv")
clean_Maine_dates(Maine_dates)




