import re
import pandas as pd
from unidecode import unidecode
from flashtext import KeywordProcessor 
import json

# alay_dict1 = pd.read_csv('https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv')
# alay_dict = alay_dict1.groupby('formal')['slang'].apply(list).to_dict()
f = open('kamus_alay.json')
alay_dict = json.load(f)
keyword_processor = KeywordProcessor()
keyword_processor.add_keywords_from_dict(alay_dict)

def _toLower(s): return s.lower()

def _remove_punct(s): 
    s = re.sub('[()!?]', ' ', s)
    s = re.sub('\[.*?\]',' ', s)
    s = re.sub(r"[^\w\d\s]+", "", s)
    s = re.sub(r"[^a-z0-9]"," ", s)
    return s

def _remove_space(s): 
    s = re.sub(' +', ' ', s)
    s = s.strip()
    return s

def _remove_link(s):
    s = re.sub(r'http\S+', '', s)
    s = re.sub(r"www.\S+", "", s)
    return s

def _remove_hastag(s):
    s = re.sub("@[A-Za-z0-9_]+","", s)
    s = re.sub("#[A-Za-z0-9_]+","", s)
    return s

def _remove_another_text(s):
    s = re.sub(r"rt", "", s)
    s = re.sub(r"user", "", s)
    s = re.sub(r'[^\x00-\x7f]',r'', s)
    return s

def _remove_another_file(s): 
    s = re.sub(r"rt", "", s)
    s = re.sub(r"user", "", s)
    return re.sub(r"\\x[A-Za-z0-9./]+", "", unidecode(s))

#Replace slang words
def _normalization(s):
    return keyword_processor.replace_keywords(s)