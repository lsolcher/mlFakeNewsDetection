from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from backend.dnnAnalysis import analyzer
from backend.scraping import scraper
from backend.bowAnalysis import bow
from backend import constants
import requests
import pickle


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = False
CORS(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/analyzeDNN')
def analyzeDNN():
    user_input = request.args.get('input')
    result = analyzer.analyze_input(user_input)
    response = {
        'result': result
    }
    return jsonify(response)


@app.route('/api/createBOW')
def createBow():
    result = bow.create_bow_model()
    response = {
        'result': result
    }
    return jsonify(response)


@app.route('/api/getBOW')
def getBOW():
    user_input = request.args.get('input')
    result = bow.analyse_bow(user_input)
    response = {
        'result': result
    }
    return jsonify(response)


@app.route('/api/bow_progress')
def bow_progress():
    with open(constants.PROGRESSFILE_BOW, 'rb') as fp:
        progress = pickle.load(fp)
        print(jsonify(progress))
    return jsonify(progress)


@app.route('/api/scrape')
def scrape():
    result = scraper.scrape()
    response = {
        'result': result
    }
    return jsonify(response)

@app.route('/api/scrape_progress')
def scrape_progress():
    with open(constants.PROGRESSFILE, 'rb') as fp:
        progress = pickle.load(fp)
        print(jsonify(progress))
    return jsonify(progress)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")