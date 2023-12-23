from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from t2i import gen
from i2i import fix
app = Flask(__name__)

CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/t2i', methods=['POST'])
def t2i():
    data = request.get_json()
    input_text = data.get('text')
    step = data.get('step')
    if input_text:
        generated = gen(input_text, step)
        return jsonify({'image': generated})


@app.route('/i2i', methods=['POST'])
def i2i():
    data = request.get_json()
    input_text = data.get('text')
    if input_text:
        generated = fix(input_text)
        return jsonify({'images': generated})


if __name__ == '__main__':
    app.run()
