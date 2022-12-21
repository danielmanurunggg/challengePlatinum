import re
import pandas as pd
from unidecode import unidecode

kamus = pd.read_csv('data/new_kamusalay.csv', names = ['sebelum', 'sesudah'], encoding='latin-1')

number = 0

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

def _normalization(s):
  global number
  words = s.split()
  clear_words = ""
  for val in words:
    x = 0
    for idx, data in enumerate(kamus['sebelum']):
      if(val == data):
        clear_words += kamus['sesudah'][idx] + ' '
        print(number,"Transform :",data,"-",kamus['sesudah'][idx])
        x = 1
        number += 1
        break
    if(x == 0):
      clear_words += val + ' '
  return clear_words