from flask import Flask, request
from flask_cors import CORS, cross_origin
import flask

import os
import pandas as pd
from translation_utils import Translator

ROOT = os.path.join(os.getcwd())
print(ROOT)

PORT = 5000

flask_app = Flask(__name__)

CORS(flask_app, resources={r"/*": {"origins": f"http://localhost:{PORT}"}})
CORS(flask_app)

@flask_app.route('/')
def Home():
    """
    Home URL
    """

    return "Ok", 200

@flask_app.route('/translate/<model_name>/', methods=['POST'])
def translate(model_name='MBart'):
    valid_models = ['MBart', 'SeamlessM4T']

    if model_name in valid_models:
        model = Translator(model_name)
    else:
        return f'{model_name} not supported', 500

    body = request.get_json()

    if body and len(body) != 0:
        results = pd.DataFrame(body)
        results = results.apply(lambda row: model.translate(row), axis=1)

        return results[['Translated']].to_dict(orient='records')
    else:
        return "Input data needed", 500
    
if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)