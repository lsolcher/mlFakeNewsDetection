from flask import Flask, render_template, jsonify, request
from random import *
from flask_cors import CORS
from backend.analysis import main
import requests


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = False
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/analyze')
def analyze():
    user_input = request.args.get('input')
    result = main.analyze_input(user_input)
    response = {
        'result': result
    }
    return jsonify(response)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")