from functions import *

recent = pd.read_csv('recent.csv').set_index('state')
#data_breach_chronology = pd.read_csv('data_breach_chronology.csv')
data_breach_chronology = pd.DataFrame()
#Oregon
or_df, or_recent = update_Oregon(recent['recent']['Oregon'])
recent['recent']['Oregon'] = or_recent
data_breach_chronology.append(or_df)


recent.to_csv('recent.csv')
data_breach_chronology.to_csv('data_breach_chronology.csv')