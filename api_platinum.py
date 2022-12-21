from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import time
from clean_data import _toLower, _remove_punct, _remove_space, _remove_link, _remove_hastag, _normalization, _remove_another_text, _remove_another_file
from predictLSTM import predictText_LSTM, predictFile_LSTM
import pandas as pd
from database import inputdatabaseTextLSTM, inputdatabaseFileLSTM
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

@swag_from("docs/swagger_config_text_lstm.yml", methods=['POST'])
@app.route("/api/v1/lstm/text", methods=['POST'])
def predict_text():
    text = request.get_json() # get text
    text_clean = text_processing(text['text']) # membersihkan text
    result = predictText_LSTM(text_clean) # prediksi text
    inputdatabaseTextLSTM(text_clean, result) # input ke database
    return jsonify({"text":text_clean,"result":result}) # response api

@swag_from("docs/swagger_config_file_lstm.yml", methods=['POST'])
@app.route("/api/v1/lstm/file", methods=['POST'])
def file_cleaning():
    start_time = time.time()
    file = request.files['file']
    df = pd.read_csv(file, names=['text'], encoding=('ISO-8859-1'))
    df['result'] = predictFile_LSTM(df)
    inputdatabaseFileLSTM(df)
    print(df)
    # inputdatabaseFileLSTM(df, result)
    return jsonify({"result":"file berhasil diupload ke database","time_exc":"--- %s seconds ---" % (time.time() - start_time)})

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan