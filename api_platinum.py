from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
app = Flask(__name__) # deklarasi Flask
app.json_encoder = LazyJSONEncoder

swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API TESTER'),
        'version': LazyString(lambda: '1'),
        'description': LazyString(lambda: 'API Tester for challenge')
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

if __name__ == "__main__":
    app.run(port=1234, debug=True) # debug ==> kode otomatis update ketika ada perubahan