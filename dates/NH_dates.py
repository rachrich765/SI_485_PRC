from datetime import datetime
import pandas as pd
import csv
import arrow
import re
from datetime import date
import dateutil.parser
new_NH_dates = list()
new_NH_dates2 = list()
new_NH_dates3 = list()
new_NH_dates4 = list()
new_NH_dates5 = list()
def clean_NH_data(NH_data):
	NH_data = NH_data
	for x in NH_data['Dates of Breach']:
		x = str(x)
		try: 
			d = datetime.strptime(x, "%d-%b-%y")
			new_NH_dates.append(d)
		except:	
			new_NH_dates.append(x)
	
	NH_data['Start Date of Breach'] = new_NH_dates
	
	for x in NH_data['Start Date of Breach']:
		try: 
			d = datetime.strptime(x, "%B %d, %Y")
			new_NH_dates2.append(d)
		except:	
			new_NH_dates2.append(x)

	NH_data['Start Date of Breach'] = new_NH_dates2

	for x in NH_data['Start Date of Breach']:
		try: 
			d = datetime.strptime(x, "%B %d. %Y")
			new_NH_dates3.append(d)
		except:	
			new_NH_dates3.append(x)

	NH_data['Start Date of Breach'] = new_NH_dates3
	for x in NH_data['Start Date of Breach']:
		try: 
			d = datetime.strptime(x, "%B %d %Y")
			new_NH_dates4.append(d)
		except:	
			new_NH_dates4.append(x)

	NH_data['Start Date of Breach'] = new_NH_dates4
	for x in NH_data['Start Date of Breach']:
		try: 
			d = datetime.strptime(x, "%B %d,%Y")
			new_NH_dates5.append(d)
		except:	
			new_NH_dates5.append(x)
	NH_data['Start Date of Breach'] = new_NH_dates5
	NH_data['End Date of Breach'] = ''
	NH_data.to_csv("testNH.csv")
	return NH_data

# replace with NH data
y = pd.read_csv('C:/Users/atrm1/Downloads/NH.csv')
clean_NH_data(y)
