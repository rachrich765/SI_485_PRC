def try_notice_headers_datatype(text):
    text_format = text
    text = text.replace('\n','')
    notice_headers = ['what happened','what we are doing', 'what information was involved', 
                      'what you can do', 'for more information', 'what personal information was involved']
    working = [True for x in notice_headers if x in text]
    l = []
    
    if working:
        k = text.index(notice_headers[2])

        try:
            l.append(text.index(notice_headers[3]))
        except:
            pass
        try:
            l.append(text.index(notice_headers[4]))
        except:
            pass
        try:
            l.append(text.index(notice_headers[5]))
        except:
            pass
        
        l = sorted(l)
        min_idx = k
        new_l = [n for n,i in enumerate(l) if i>min_idx ][0]
        source = text[k:l[new_l]]       
        return source
    else: 
        return False

def find_datatype_breached(pdf_text):
  potentially_stolen_datatype = ['social security number', "driver's license", "passport", "state id", "license",
                               'name', 'date of birth', 'dates of birth', "gender", 
                               'credit card', "debit card", "payment",
                               "financial", "security code", "verification code", "cvv", "date of card expiration", "expiration date",
                               "login", "password", "user name", "username", "log in"  
                               "telephone number", "email", "phone number", "address",
                               "medical", "blood type", "donor profile",
                               "insurance",
                                "profile", "id number", "identification number",
                              "ip address"]
  negation = ['no','not',"wasn't"]
  sentences = pdf_text.split('.')
  sents = []
  for sentence in sentences:
      for item in datatypes:
          if item in sentence:
              sents.append(sentences.index(sentence))

  del_ind = []
  for ind in sents:
      for item in negation: 
          if item in sentences[ind]:
              del_ind.append(ind)

  del_ind = sorted(set(del_ind), reverse=True)

  for ind in del_ind:
      del sentences[ind]
  k = '.'.join(sentences)
  stolen_list = [x for x in potentially_stolen_datatype if x in k]
  return stolen_list
