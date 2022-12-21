import pickle
import numpy as np
import pandas as pd
from keras_preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

with open('data/tokneizerLSTM.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

Model=load_model('data/lstmModel.h5')

def predictText_LSTM(text):
    print(text)
    text = tokenizer.texts_to_sequences([text])
    text = pad_sequences(text, maxlen=150)
    print(text)
    sentiment = Model.predict(text)[0]
    if(np.argmax(sentiment) == 0):
        return "negative"
    elif (np.argmax(sentiment) == 1):
        return "neutral"
    elif (np.argmax(sentiment) == 2):
        return "positive"

def predictFile_LSTM(X_test):
    print(X_test)
    Y_predict = []
    for index, row in X_test.iterrows():
        print(row["text"])
        sequences_X_test = tokenizer.texts_to_sequences([row["text"]])
        X_test_1 = pad_sequences(sequences_X_test, maxlen=150)
        print(X_test_1)
        x = np.reshape(X_test_1, (1,150))
        result = Model.predict(x, batch_size=1, verbose=2)[0]
        if(np.argmax(result) == 0):
            Y_predict.append("negative")
        elif (np.argmax(result) == 1):
            Y_predict.append("neutral")
        elif (np.argmax(result) == 2):
            Y_predict.append("positive")
    return Y_predict