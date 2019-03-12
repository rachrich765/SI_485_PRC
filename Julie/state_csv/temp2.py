import pandas as pd

columns = ['Name of Entity', 'Dates of Breach', 'Reported Date',
       'Date(s) of Discovery of Breach', 'Date Notice Provided to Consumers',
       'Data Stolen', "Who's Affected",'Entity Address', 'Type of Breach','Individuals Affected',
       'Location of Breached Information','Details', 'Entity Type','State Reported','Link to PDF',
       'PDF text (ALL)']
data_breach_chronology = pd.DataFrame(columns=columns)

delaware = pd.read_csv('delaware.csv')
data_breach_chronology = data_breach_chronology.append(delaware,ignore_index=True)

indiana = pd.read_csv('indiana.csv')
data_breach_chronology = data_breach_chronology.append(indiana,ignore_index=True)

maine = pd.read_csv('maine.csv')
data_breach_chronology = data_breach_chronology.append(maine,ignore_index=True)

oregon = pd.read_csv('oregon.csv')
data_breach_chronology = data_breach_chronology.append(oregon,ignore_index=True)

vermont = pd.read_csv('vermont.csv')
data_breach_chronology = data_breach_chronology.append(vermont,ignore_index=True)


wisconsin = pd.read_csv('wisconsin.csv')
data_breach_chronology = data_breach_chronology.append(wisconsin,ignore_index=True)

washington = pd.read_csv('washington.csv')
data_breach_chronology = data_breach_chronology.append(washington,ignore_index=True)

california = pd.read_csv('california.csv')
data_breach_chronology = data_breach_chronology.append(california,ignore_index=True)

iowa = pd.read_csv('iowa.csv')
data_breach_chronology = data_breach_chronology.append(iowa,ignore_index=True)

data_breach_chronology.to_csv('data_breach_chronology.csv')