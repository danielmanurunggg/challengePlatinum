from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import time
from clean_data import _toLower, _remove_punct, _remove_space, _remove_link, _remove_hastag, _normalization, _remove_another_text, _remove_another_file
from predictLSTM import predictText_LSTM, predictFile_LSTM
from predictANN import predictText_ANN, predictFile_ANN
import pandas as pd
from database import inputdatabaseTextLSTM, inputdatabaseFileLSTM, inputdatabaseTextANN, inputdatabaseFileANN

app = Flask(__name__) # deklarasi Flask
app.json_encoder = LazyJSONEncoder

def text_processing(s):
    text = s
    s = _toLower(s)
    s = _remove_link(s)
    s = _remove_another_text(s)
    s = _remove_hastag(s)
    s = _remove_punct(s)
    s = _normalization(s)
    s = _remove_space(s)
    return s

swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API TESTER'),
        'version': LazyString(lambda: '1'),
        'description': LazyString(lambda: 'API Tester for challenge platinum')
    },
    host = LazyString(lambda: request.host)
)

swagger_config = {
    "headers":[],
    "specs": [
        {
            "endpoint":"docs",
            "route":"/docs.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True
        }
    ],
    "static_url_path":"/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger = Swagger(app, template=swagger_template,config=swagger_config)

# API for ANN
@swag_from("docs/swagger_config_text_ann.yml", methods=['POST'])
@app.route("/api/v1/ann/text", methods=['POST'])
def predict_text_ann():
    text = request.get_json() # get text
    text_clean = text_processing(text['text']) # membersihkan text
    result = predictText_ANN(text_clean) # prediksi text
    inputdatabaseTextANN(text_clean, result) # input ke database
    return jsonify({"text":text_clean,"result":result}) # response api

@swag_from("docs/swagger_config_file_ann.yml", methods=['POST'])
@app.route("/api/v1/ann/file", methods=['POST'])
def predict_file_ann():
    start_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, names=['text'], encoding=('ISO-8859-1'))
    df['result'] = predictFile_ANN(df)
    inputdatabaseFileANN(df)
    return jsonify({"result":"file berhasil diupload ke database","time_exc":"--- %s seconds ---" % (time.time() - start_time)})

# API for LSTM
@swag_from("docs/swagger_config_text_lstm.yml", methods=['POST'])
@app.route("/api/v1/lstm/text", methods=['POST'])
def predict_text_lstm():
    text = request.get_json() # get text
    text_clean = text_processing(text['text']) # membersihkan text
    result = predictText_LSTM(text_clean) # prediksi text
    inputdatabaseTextLSTM(text_clean, result) # input ke database
    return jsonify({"text":text_clean,"result":result}) # response api

@swag_from("docs/swagger_config_file_lstm.yml", methods=['POST'])
@app.route("/api/v1/lstm/file", methods=['POST'])
def predict_file_lstm():
    start_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, names=['text'], encoding=('ISO-8859-1'))
    df['result'] = predictFile_LSTM(df)
    inputdatabaseFileLSTM(df)
    return jsonify({"result":"file berhasil diupload ke database","time_exc":"--- %s seconds ---" % (time.time() - start_time)})

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan