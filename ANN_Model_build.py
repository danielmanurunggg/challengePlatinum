# -*- coding: utf-8 -*-
"""Platinum ann 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jzyj_VlT4Dxe8u8ZzGX7tVZRGpeAjlxT
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split
import tensorflow.keras as keras
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from sklearn.neural_network import MLPClassifier
import pickle
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

import re
from unidecode import unidecode

from flask import Flask, request,jsonify, render_template
from flasgger import Swagger, LazyString, LazyJSONEncoder,swag_from
import sqlite3

def remove_punct(s):
    s=s.lower()
    s = re.sub(r"\\x[A-Za-z0-9./]+", '', unidecode(s))
    s = re.sub(' +', ' ',s)
    return re.sub(r"[^\w\d\s]+","",s)


def remove_emojis(data):
    emoji = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return re.sub(emoji,'',data)
def remove_range_string(data): 
    return re.sub(r'[^\x00-\x7f]','', data)

def tokenizer (x) :
  max_fatures = 2000
  tokenizer = Tokenizer(num_words=max_fatures, split=' ')
  tokenizer.fit_on_texts(x)
  X = tokenizer.texts_to_sequences(x)
  X = pad_sequences(X)
  pickle.dump(tokenizer, open('tokenizer.pkl', 'wb'))
  return X

def train_test(X,Y):
  X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.15, random_state=2022)
  return X_train, X_test, Y_train, Y_test

def model_ann (X_train, Y_train,X_test, Y_test) :
  sc_X = StandardScaler()
  X_train = sc_X.fit_transform(X_train)
  X_test = sc_X.transform(X_test)
  classifier = MLPClassifier(hidden_layer_sizes=(256,128,64,32), activation = "relu", random_state=1, solver="adam", alpha=1e-5, early_stopping=True, max_iter=1000, verbose=True)
  histroy =  classifier.fit(X_train, Y_train)
  
  df_results = pd.DataFrame(data=np.zeros(shape=(1,3)), columns = ['classifier', 'train_score', 'test_score'] )
  train_score = classifier.score(X_train, Y_train)
  test_score = classifier.score(X_test, Y_test)

  df_results.loc[1,'classifier'] = "MLP"
  df_results.loc[1,'train_score'] = train_score
  df_results.loc[1,'test_score'] = test_score
  print(df_results)
  pickle.dump(classifier, open('ANN.pkl', 'wb'))
  y_pred=classifier.predict(X_test)
  score = accuracy_score(Y_test,y_pred)


  return print(classification_report(Y_test, y_pred)), print(score)

def split(x):
  x=x.split()
  x=len(x)
  return x

def testing_sentence (twt):
  twt= remove_punct(twt)
  twt= remove_emojis(twt)
  twt=re.sub(r"[\t|\n|\r]"," ", twt)
  tokenizer = pickle.load(open('tokenizer.pkl','rb'))
  twt = tokenizer.texts_to_sequences(twt)
  twt = pad_sequences(twt, maxlen=78, dtype='int32', value=0)
  classifier = pickle.load(open('ANN.pkl','rb'))
  sentiment = classifier.predict(twt)
  if(np.argmax(sentiment) == 2):
      a="negative"
  elif (np.argmax(sentiment) == 1):
      a=("positive")
  elif (np.argmax(sentiment) == 0):
      a=("Netral")

  return a

data= pd.read_csv("train_preprocess.tsv",names=["review","label"], sep ="\t")
df_tsv = pd.DataFrame(data)
data

data["review"]= data["review"].apply(remove_emojis)
data["review"]= data["review"].apply(remove_punct)
data["review"]=data["review"].replace([r"\\t|\\n|\\r"], " ", regex=True)
data

label = {"neutral":0,"positive":1,"negative":2}
data["label"]=data["label"].map(label)
data

data["len"]= data["review"].apply(split)
data["len"].describe()

"""#Membuang outlayer

"""

q75,q25 =np.percentile(data['len'],[75,25])
intr_qr = q75-q25
max = q75+(1.5*intr_qr)
min = q25-(1.5*intr_qr)
a = data['len'].size
for i in range(a):
  if data['len'].loc[i]<min or data['len'].loc[i]>max:
    data['len'].loc[i]=0
data = data[data.len != 0]

a=data['label'].value_counts()
a=pd.DataFrame(a)
sns.barplot(y=a["label"], x=a.index)

X = tokenizer(data["review"])
Y = pd.get_dummies(data['label']).values

"""#Over Sampling """

from imblearn.over_sampling import RandomOverSampler
from collections import Counter
over_sampler = RandomOverSampler(random_state=42)
X, Y = over_sampler.fit_resample(X, Y)

a=pd.DataFrame(Y)
a=a.sum(axis=0)
a=pd.DataFrame(a)
sns.barplot(y=a[0], x=a.index)

print([sum(x) for x in zip(*Y)])

X_train, X_test, Y_train, Y_test = train_test (X,Y)



a=pd.DataFrame(Y_train)
a=a.sum(axis=0)
a=pd.DataFrame(a)
sns.barplot(y=a[0], x=a.index)

print(X_train.shape,Y_train.shape)
print(X_test.shape,Y_test.shape)

"""#Train Model

"""

model_ann (X_train, Y_train,X_test, Y_test)



twt = 'suara kamu tidak enak untuk di dengar'
#vectorizing the tweet by the pre-fitted tokenizer instance
sentiment=testing_sentence (twt)
print(sentiment)

"""# SQL & SWAGGER

"""

conn = sqlite3.connect ("sqlite3_ann_text.db")
# conn.execute("create table text (input_text varchar, label varchar);")
conn.close()

app = Flask (__name__)
app.json_encoder =LazyJSONEncoder

swagger_template = dict(
info = {
    'title': LazyString(lambda: 'percobaan membuat api swagger'),
    'version': LazyString(lambda: '1'),
    'description': LazyString(lambda: 'coba-coba'),
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger= Swagger(app, template=swagger_template,config=swagger_config)

@swag_from("swagger_ann_text.yml", methods=['POST'])
@app.route("/ann_text/v1",methods=["POST"])
def cleansing_text():
    s=request.get_json()
    sentiment=testing_sentence (s["text"])
    conn = sqlite3.connect ("sqlite3_ann_text.db")
    add='''insert into text (input_text, label) values (?,?);'''
    conn.execute(add,(s["text"],sentiment))
    conn.commit()
    conn.close()
    return jsonify({"Result" : sentiment})

# conn = sqlite3.connect ("sqlite3_ann_csv.db")
# conn.execute("create table text (input_text varchar, label varchar);")
# conn.close()

@swag_from("swagger_upload_csv.yml", methods=['POST'])
@app.route("/upload_csv/v1",methods=["POST","GET"])
def cleansing_csv():
    f = (request.files.get("file"))
    df= pd.read_csv(f,names=["review","label"], sep ="\t")
    df_csv = pd.DataFrame(df)
    # conn = sqlite3.connect ("sqlite3_csv.db")
    # df_csv.to_sql("csv", con=conn,index=False,if_exists="replace")
#     conn.close()
    df_csv["review"]= df_csv["review"].apply(testing_sentence).str.lower()
#     df_csv["Tweets"]= df_csv["Tweets"].apply(remove_multi_space)
#     conn = sqlite3.connect ("sqlite3_csv.db")
#     df_tweet.to_sql("csv", con=conn,index=False,if_exists="replace")
#     conn.close()
    # eksport dv to csv
#     json = df_tweet["Tweets"].head().to_json()
#     df_tweet['Tweets_2'] = df_tweet.Tweets.apply(remove_stopwords) 
#     df_hs= df[(df["HS_Weak"]==1)&(df["HS_Individual"]==1)]
#     text =" ".join(df_hs["Tweets_2"]) # menggabungkan semua text menjadi 1 string
#     wordcloud=WordCloud().generate(text)
#     plt.imshow(wordcloud)
#     plt.show()
#     return jsonify({"Result" : json, "Lama Eksekusi":lama_eksekusi})

if __name__=="__main__":
    app.run(port=1234,debug=True)