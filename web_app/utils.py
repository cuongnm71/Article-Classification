import re
import string

def preprocess(s):
    for ch in string.punctuation:                                                                                                     
        s = s.replace(ch, " ") 
    s = s.replace(ch, "'") 
    s = re.sub("\s\s+", " ", s)
    s = re.sub("\s\d+(?=\s)", "", s)
    s = re.sub("\s\d{1,2}h\d{1,2}", "", s) #remove time
    s = s.lower()
    return s