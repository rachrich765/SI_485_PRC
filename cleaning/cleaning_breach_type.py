
# coding: utf-8

# In[46]:

import pandas as pd
import string
import re
import numpy as np

from six.moves import cPickle as pickle

import nltk
from nltk.corpus import stopwords

import sklearn
from sklearn import model_selection, preprocessing, naive_bayes
from sklearn.feature_extraction.text import CountVectorizer

with open('nb_breach_type_large.pkl', 'rb') as fid:
    l_nb_loaded = pickle.load(fid)
l_vecs = pd.read_csv('large_count_vectors.csv')

from collections import Counter


# In[92]:

def get_breach_type_cause(large_df):
    master = large_df
    causes_sorted_1 = []
    causes = list(master["Cause of Breach"].fillna("NONE"))
#     print(causes)
    pdfs = master["PDF text (ALL)"] 
    words_for_1 = ['unauthorized', 'fraud', 'attack', 'malicious', 'compromise', 'suspicious', 'malware', 'ransomware', 
               'cyber', 'authorization', 'phishing', 'cybersecurity', 'infected', 'compromised',
               'virus', 'compromise', 'attacked', 'hacked', 'spoofing', 'scam', 'scammer', 'network', 'fraudulent', 'email',
               'e-mail', 'emails', 'e-mails', 'phish', 'attack', 'without', 'cyberattack', 'fraudster', 'discovered',
               'system', 'systems', 'third-party', 'third', 'party']
    words_for_2 = ['contractor', "inside", 'insider', 'former']
    words_for_3 = ['papers', 'paper', 'letter']
    words_for_4 = ["laptop", "phone", 'hard', 'drive', 'laptops', 'car', 'cars', 'theft']
    words_for_5 = ["computer", "server"]
    words_for_6 = ["inadvertently", 'mistake', 'accident', 'mistakenly', 'mistaken', 'accidentally']
    try: 
        for cause in causes:
            if cause == 'NONE':
                causes_sorted_1.append("UND")
                continue
            cause = cause.lower()
            cause = re.sub('[^\w\s]','',cause)
            cause = cause.split(' ')
            a = [x for x in cause if x in words_for_1]
            b = [x for x in cause if x in words_for_2]
            c = [x for x in cause if x in words_for_3]
            d = [x for x in cause if x in words_for_4]
            e = [x for x in cause if x in words_for_5]
            f = [x for x in cause if x in words_for_6]
            tup = (len(a),len(b),len(c),len(d),len(e),len(f))
            if max(tup) != 0:
                causes_sorted_1.append(tup.index(max(tup))+1)
            if max(tup) == 0: 
                causes_sorted_1.append(7)
    except:
        causes_sorted_1.append("UND")
            
    return causes_sorted_1
# l has "UND" for not yet determined


# In[93]:

def clean_pdf_text(pdf_text):
    modified = stopwords.words('english')
    modified.extend(['information','happened', 'january', 'february', 'march', 'april',
                'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'])
#     print(modified)
    text = pdf_text
#     print(text)
    t = re.sub(r'[^\w\s]','',text)
    t = re.sub("[^A-z\s]",'',t)
    t = re.sub('\?','',t)
    t = re.sub(r'[0-9]','',t)
    k = t.split(' ')
#     print(k)
#     k = list(filter(None, k))
    no_stop = [x for x in k if x not in modified]
    b = [item.strip() for item in no_stop]
    a = [item for item in b if item != '']
    no_st = ' '.join(a)
    return no_st


# In[319]:

def get_breach_type_classifier(large_df, l_vecs = l_vecs, l_nb = l_nb_loaded):
    causes_sorted_2 = []
    words_for_1 = ['unauthorized', 'fraud', 'attack', 'malicious', 'compromise', 'suspicious', 'malware', 'ransomware', 
               'cyber', 'authorization', 'phishing', 'cybersecurity', 'infected', 'compromised',
               'virus', 'compromise', 'attacked', 'hacked', 'spoofing', 'scam', 'scammer', 'network', 'fraudulent', 'email',
               'e-mail', 'emails', 'e-mails', 'phish', 'attack', 'without', 'cyberattack', 'fraudster', 'discovered',
               'system', 'systems', 'third-party', 'third', 'party', 'hacking'
              ]
    words_for_2 = ['contractor', 'insider', 'former']
    words_for_3 = ['papers', 'paper', 'letter']
    words_for_4 = ["laptop", "phone", 'hard', 'drive', 'laptops', 'car', 'cars']
    words_for_5 = ["computer", "server"]
    words_for_6 = ["inadvertently", 'mistake', 'accident', 'mistakenly', 'mistaken', 'accidentally']

    others = words_for_2 + words_for_3 + words_for_4 + words_for_5 + words_for_6 
    trig = others+words_for_1
    pdfs = list(large_df["PDF text (ALL)"].fillna("no_pdf"))
    for pdf in pdfs:
        if pdf == "no_pdf":
            causes_sorted_2.append("UND")
        else:
            p = clean_pdf_text(pdf)  
            c = p.split()
            a = Counter(c)
#             print(a)
            features = []  
            k = list(l_vecs.columns)[1:-1]
            for word in k:
                if word in a:
                    features.append(a[word])
                else:
                    features.append(0)
#             print(features)    
            feat_list = features
            features = np.array(features)
            for feat in a:
#                 print(feat)
                try:
                    if feat in trig:
#                         print('multi')
                        i = k.index(feat)
                        features[i] = features[i]*1000
#                         print(features[i])
                except:
                    pass
            prediction = l_nb.predict(features.reshape(1,-1))
            prediction = int(prediction)
            if prediction == 0:
                causes_sorted_2.append(1)
            else:
                p = p.split(' ')
                words_for_1 = ['unauthorized', 'fraud', 'attack', 'malicious', 'compromise', 'suspicious', 
                               'malware', 'ransomware', 
               'cyber', 'authorization', 'phishing', 'cybersecurity', 'infected', 'compromised',
               'virus', 'compromise', 'attacked', 'hacked', 'spoofing', 'scam', 'scammer', 'network', 'fraudulent', 
                'phish', 'attack', 'cyberattack', 
                'fraudster', 'third-party', 'hacking'
              ]

                b = [x for x in p if x in words_for_2]
                d = [x for x in p if x in words_for_4]
                print(d)
                e = [x for x in p if x in words_for_5]
                f = [x for x in p if x in words_for_6]
                tup = (len(b),len(d),len(e),len(f))
                opt = [2,4,5,6]
                if len(f)!= 0:
                    causes_sorted_2.append(6)
                if max(tup) != 0:
                    causes_sorted_2.append(opt[tup.index(max(tup))])
                elif max(tup) == 0: 
                    causes_sorted_2.append(7)
                    
            
    return causes_sorted_2

# In[330]:

##l1 = result of running get_breach_type_cause
## l2 = result of running second function

def final_list(l1, l2):
    assert len(l1) == len(l2)
    final = []
    for i in range(0, len(l1)):
        item = l1[i]
        if item != "UND":
            final.append(item)
        else:
            m = l2[i]
            if type(m) == int:
                final.append(item)
            else:
                final.append(7)
    return final 


# In[ ]:



