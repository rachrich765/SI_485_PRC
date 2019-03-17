import re
import pandas as pd
x = pd.read_csv("newhampshire.csv")

#example = 'A&A Global Imports, Inc., January 9, 2019'
#pattern = r'(.*?)([A-Za-z]{3,10}\s*[0-9]{1,2}[,/.]*\s*[0-9]{4})'
#print(re.findall(pattern,example)[0])
def get_date(row):
	pattern = r'.*?([A-Za-z]{3,10}\s*[0-9]{1,2}[,/.]*\s*[0-9]{4})'
	try:
		match = re.findall(pattern,row)[0]
		return match
	except:
		return ''
def get_company(row):
	pattern = r'(.*?)[A-Za-z]{3,10}\s*[0-9]{1,2}[,/.]*\s*[0-9]{4}'
	try:
		match = re.findall(pattern,row)[0]
		return match
	except:
		return row

#x['Dates of Breach'] = x['company_date'].apply(lambda x: re.findall(pattern, x)[0])
x['Dates of Breach'] = x['company_date'].apply(get_date)
x['Name of Entity'] = x['company_date'].apply(get_company)
x = x.drop(['Unnamed: 0','company_date'], axis = 1)
x.to_csv('test.csv')