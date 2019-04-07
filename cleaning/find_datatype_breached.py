def find_datatype_breached(pdf_text):
    datatypes = ['social security number', "driver's license", "passport", "state id", "license",
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
    if len(stolen_list) == 0:
        stolen_list = "UNK"
    return stolen_list
