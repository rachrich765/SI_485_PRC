from functions import *

recent = pd.read_csv('recent.csv').set_index('state')
#data_breach_chronology = pd.read_csv('data_breach_chronology.csv')

columns = ['Name of Entity', 'Dates of Breach', 'Reported Date',
       'Date(s) of Discovery of Breach', 'Date Notice Provided to Consumers',
       'Data Stolen', "Who's Affected", 'Type of Breach','Individuals Affected',
       'Location of Breached Information','Details', 'Entity Type','State Reported','Link to PDF',
       'PDF text (ALL)']
data_breach_chronology = pd.DataFrame(columns=columns)

#Oregon
or_df, or_recent = update_Oregon(recent['recent']['Oregon'])
recent['recent']['Oregon'] = or_recent
data_breach_chronology = data_breach_chronology.append(or_df,ignore_index=True)
print ('\n', 'Fetched Oregon Data', '\n')

#Wisconsin
wi_df, wi_recent = update_Wisconsin(recent['recent']['Wisconsin'])
recent['recent']['Wisconsin'] = wi_recent
data_breach_chronology = data_breach_chronology.append(wi_df,ignore_index=True)
print ('\n', 'Fetched Wisconsin Data', '\n')

#Vermont
vt_df, vt_recent = update_Vermont(recent['recent']['Vermont'])
recent['recent']['Vermont'] = vt_recent
data_breach_chronology = data_breach_chronology.append(vt_df,ignore_index=True)
print ('\n', 'Fetched Vermont Data', '\n')

#Washington
wa_df, wa_recent = update_Washington(recent['recent']['Washington'])
recent['recent']['Washington'] = wa_recent
data_breach_chronology = data_breach_chronology.append(wa_df,ignore_index=True)
print ('\n', 'Fetched Washington Data', '\n')

#California
ca_df, ca_recent = update_California(recent['recent']['California'])
recent['recent']['California'] = ca_recent
data_breach_chronology = data_breach_chronology.append(ca_df,ignore_index=True)
print ('\n', 'Fetched California Data', '\n')

#Indiana

#Iowa

#Delaware

#New Hampshire

#New Jersey

#US Department of Health
usdh_df, usdh_recent = update_USDeptHealth(recent['recent']['Department of Health'])
recent['recent']['Department of Health'] = usdh_recent
data_breach_chronology = data_breach_chronology.append(usdh_df,ignore_index=True)
print ('\n', 'Fetched USDH Data', '\n')

#print (data_breach_chronology.head())

recent.to_csv('recent.csv')
data_breach_chronology.to_csv('data_breach_chronology.csv')
