from functions import *

recent = pd.read_csv('recent.csv').set_index('state')
#data_breach_chronology = pd.read_csv('data_breach_chronology.csv')

columns = ['Name of Entity', 'Dates of Breach', 'Reported Date',
       'Date(s) of Discovery of Breach', 'Date Notice Provided to Consumers','Data Stolen', "Who's Affected", 'Details', 'State Reported']
data_breach_chronology = pd.DataFrame(columns=columns)

#Oregon
or_df, or_recent = update_Oregon(recent['recent']['Oregon'])
recent['recent']['Oregon'] = or_recent
data_breach_chronology = data_breach_chronology.append(or_df)


wi_df, wi_recent = update_Wisconsin(recent['recent']['Wisconsin'])
recent['recent']['Wisconsin'] = wi_recent
data_breach_chronology = data_breach_chronology.append(wi_df)

print (data_breach_chronology.head())

recent.to_csv('recent.csv')
data_breach_chronology.to_csv('data_breach_chronology.csv')
