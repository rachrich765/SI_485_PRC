from datetime import datetime
import pandas as pd
import csv
import arrow
import re
from datetime import date
import dateutil.parser

def NJ_clean_dates(NJ_data):
	new_NJ_dates = list()
	NJ_data = NJ_data
	for x in NJ_data['Dates of Breach']:
		x = str(x)
		try: 
			d = datetime.strptime(x, "%d-%b-%y")
			new_NJ_dates.append(d)
		except:	
			new_NJ_dates.append('')

	NJ_data['Start Date of Breach'] = new_NJ_dates
	NJ_data['End Date of Breach'] = ''
	NJ_data.to_csv('testNJ.csv')
	return NJ_data


# reset this to be the NJ dataframe
x = pd.read_csv('C:/Users/atrm1/Downloads/NJ_dates.csv')
NJ_clean_dates(x)

