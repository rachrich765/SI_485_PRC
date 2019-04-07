#input: finished csv file
#output: csv file with entity duplicates reduced

def clean_ents(csv_file):
    df_master = pd.read_csv(csv_file)
    entities = list(df_master["Name of Entity"].fillna("[None Named]"))
    low_ents = [x.lower() for x in entities] #make all lowercase
    low_ents = [re.sub("-databreach","",x) for x in low_ents] #removes -databreach string at end
    low_ents = [re.sub("-securitybreach","",x) for x in low_ents] #removes -securitybreach string at end
    low_ents = [re.sub("-data breach","",x) for x in low_ents] #removes -data breach string at end
    low_ents = [re.sub("data breach","",x) for x in low_ents] #removes data breach string at end
    low_ents = [re.sub("-breach notification","",x) for x in low_ents] #removes -breach notification string at end
    low_ents = [re.sub("^[0-9-]*","",x) for x in low_ents] #removes dates at start of string
    low_ents = [re.sub(",\s{0,}[0-9].*[a-z]{2}\s{1,}[0-9]{5}","",x) for x in low_ents] #removes addresses
    low_ents = [re.sub(";\s{0,}[0-9].*[a-z]{2}\s{1,}[0-9]{5}","",x) for x in low_ents] #removes addresses
    low_ents = [re.sub("\s{0,}p.o. box\s[0-9].*[a-z]{2}\s{1,}[0-9]{5}","",x) for x in low_ents] #removes addresses
    no_space_punc = {}
    for entity in low_ents:
        ent = re.sub("[\s]","",entity) #remove spaces
        ent = re.sub("[^A-z0-9]","",entity) #remove punctuation
        no_space_punc[entity] = ent
    no_space_punc_reversed = inv_map = [(v, k) for k, v in no_space_punc.items()]
#     print(len(no_space_punc_reversed))

    #making a list of duplicates
    dups = []
    simp = [x[0] for x in no_space_punc_reversed]
    for entity in simp:
        if [x[0] for x in no_space_punc_reversed].count(entity)>1:
            dups.append(entity)
    del_list = []
    for dup in dups:
        indices = sorted([i for i, x in enumerate(simp) if x == dup])
        del_list.extend(indices[1:])
    indices = list(set(sorted(del_list)))
    for i in sorted(indices, reverse=True):
        del no_space_punc_reversed [i]
    final_dict = dict(no_space_punc_reversed)
    clean_ents = []
    for entity in low_ents:
        ent = re.sub("[\s]","",entity) #remove spaces
        ent = re.sub("[^A-z0-9]","",entity) #remove punctuation
        clean_ents.append(final_dict[ent])
    df_master["Name of Entity"] = clean_ents
    return df_master
