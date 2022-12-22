import pickle
from keras_preprocessing.sequence import pad_sequences
import numpy as np

with open('data/ANN/tokenizerANN.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)


Model = pickle.load(open('data/ANN/ANN.pkl','rb'))
  
def predictText_ANN (twt):
    twt = tokenizer.texts_to_sequences([twt])
    twt = pad_sequences(twt, maxlen=78, dtype='int32', value=0)
    sentiment = Model.predict(twt)
    if(np.argmax(sentiment) == 2):
        return "negative"
    elif (np.argmax(sentiment) == 1):
        return "positive"
    elif (np.argmax(sentiment) == 0):
        return "neutral"

def predictFile_ANN(X_test):
    print(X_test)
    Y_predict = []
    for index, row in X_test.iterrows():
        print(row["text"])
        sequences_X_test = tokenizer.texts_to_sequences([row["text"]])
        X_test_1 = pad_sequences(sequences_X_test, maxlen=78)
        x = np.reshape(X_test_1, (1,78))
        result = Model.predict(x)[0]
        print(result)
        if(np.argmax(result) == 0):
            Y_predict.append("neutral")
        elif (np.argmax(result) == 1):
            Y_predict.append("positive")
        elif (np.argmax(result) == 2):
            Y_predict.append("negative")
    return Y_predict