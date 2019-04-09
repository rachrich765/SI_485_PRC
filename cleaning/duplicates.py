import pandas as pd
import csv
import re

def remove_duplicates(y):
	def clean_state(x):
	# only get words 
		m = re.search(r".*in (\w+)", str(x))
		if m is not None:
		# get name of state
			return m.group(1)
		else:
			return x

	def clean_number(x):
		# only get number of individuals affected
		m = re.search(r"([\d,]+)", str(x))
		if m is not None:
			#  strip comma from number
			return int(re.sub(",", "", m.group(1)))
		else:
			return None
	data = y
	# the line below is only needed if you're reading in a CSV
	data = data.drop(labels='Unnamed: 0', axis=1)
	# get all data where Name of Entity, Start Date, and End Date match (excluding NAs)
	duplicates = pd.concat(g for _, g in data.groupby(["Name of Entity", "Start Date", "End Date"]) if len(g) > 1)
	# remove data where individuals affected and Name of Entity are the same
	data = data.drop_duplicates(subset=["Individuals Affected", "Name of Entity"], keep='last')
	# separate name of state where individuals were affected from # of individuals affected
	data['State where Affected'] = data['Individuals Affected'].apply(lambda x: clean_state(x))
	# separate  # of individuals affected from name of state where individuals were affected 
	data['# Affected Within State'] = data['Individuals Affected'].apply(lambda x: clean_number(x))
	# get most accurate number of individuals affected if 2 are provided for the same breach
	duplicates4 = data.groupby(['Name of Entity']).agg({'# Affected Within State':'max'})
	# merge data without duplicates with original data
	joined_data = pd.merge(duplicates4, data, on=['Name of Entity', '# Affected Within State'])
	# reseave entire dataset
	joined_data.to_csv('test5.csv', index=False)
	return joined_data

# replce the csv file name with the name of our dataframe
remove_duplicates(pd.read_csv('C:/Users/atrm1/Downloads/new_dates.csv'))