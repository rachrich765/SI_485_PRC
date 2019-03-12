from functions import *

recent = pd.read_csv('recent.csv').set_index('state')
#data_breach_chronology = pd.read_csv('data_breach_chronology.csv')

columns = ['Name of Entity', 'Dates of Breach', 'Reported Date',
       'Date(s) of Discovery of Breach', 'Date Notice Provided to Consumers',
       'Data Stolen', "Who's Affected",'Entity Address', 'Type of Breach','Individuals Affected',
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
in_df, in_recent = update_Indiana(recent['recent']['Indiana'])
recent['recent']['Indiana'] = in_recent
data_breach_chronology = data_breach_chronology.append(in_df,ignore_index=True)
print ('\n', 'Fetched Indiana Data', '\n')

#Iowa
ia_df, ia_recent = update_Iowa(recent['recent']['Iowa'])
recent['recent']['Iowa'] = ia_recent
data_breach_chronology = data_breach_chronology.append(ia_df,ignore_index=True)
print ('\n', 'Fetched Iowa Data', '\n')

#Delaware
de_df, de_recent = update_Delaware(recent['recent']['Delaware'])
recent['recent']['Delaware'] = de_recent
data_breach_chronology = data_breach_chronology.append(de_df,ignore_index=True)
print ('\n', 'Fetched Delaware Data', '\n')

#New Hampshire
#nh_df, nh_recent = update_NewHampshire(recent['recent']['New Hampshire'])
#recent['recent']['New Hampshire'] = nh_recent
#data_breach_chronology = data_breach_chronology.append(nh_df,ignore_index=True)
#print ('\n', 'Fetched New Hampshire Data', '\n')

#New Jersey
#nj_df, nj_recent = update_NewJersey(recent['recent']['New Jersey'])
#recent['recent']['New Jersey'] = nj_recent
#data_breach_chronology = data_breach_chronology.append(nj_df,ignore_index=True)
#print ('\n', 'Fetched New Jersey Data', '\n')

#US Department of Health
#usdh_df, usdh_recent = update_USDeptHealth(recent['recent']['Department of Health'])
#recent['recent']['Department of Health'] = usdh_recent
#data_breach_chronology = data_breach_chronology.append(usdh_df,ignore_index=True)
#print ('\n', 'Fetched USDH Data', '\n')


#Maine
me_df, me_recent = update_Maine(recent['recent']['Maine'])
recent['recent']['Maine'] = me_recent
data_breach_chronology = data_breach_chronology.append(me_df,ignore_index=True)
print ('\n', 'Fetched Maine Data', '\n')

#Maryland
#md_df, md_recent = update_Maryland(recent['recent']['Maryland'])
#recent['recent']['Maryland'] = md_recent
#data_breach_chronology = data_breach_chronology.append(md_df,ignore_index=True)
#print ('\n', 'Fetched Maryland Data', '\n')

#Massachusetts
#ma_df, ma_recent = update_Massachusetts(recent['recent']['Massachusetts'])
#recent['recent']['Massachusetts'] = ma_recent
#data_breach_chronology = data_breach_chronology.append(ma_df,ignore_index=True)
#print ('\n', 'Fetched Massachusetts Data', '\n')

#Montana
#mt_df, mt_recent = update_Montana(recent['recent']['Montana'])
#recent['recent']['Montana'] = mt_recent
#data_breach_chronology = data_breach_chronology.append(mt_df,ignore_index=True)
#print ('\n', 'Fetched Montana Data', '\n')

#print (data_breach_chronology.head())

recent.to_csv('recent.csv')
data_breach_chronology.to_csv('data_breach_chronology.csv')
