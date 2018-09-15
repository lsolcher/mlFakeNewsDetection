from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from backend.dnnAnalysis import analyzer
from backend.scraping import scraper
from backend.bowAnalysis import bow
from backend.completeAnalysis import analyse
from backend import constants
import requests, json
import pickle


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = False
CORS(app)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

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
    """

    :return: json array
    """
    user_input = request.args.get('input')
    result = bow.get_bow_result(user_input)
    response = {
        'url': ['<a href=\"' + i[0] + '\">' + i[0] + '</a>' for i in result],
        'value': [i[1] for i in result]
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
    with open(constants.PROGRESSFILE_SCRAPER, 'rb') as fp:
        progress = pickle.load(fp)
        print(jsonify(progress))
    return jsonify(progress)


@app.route('/api/getCompleteResult')
def getCompleteResult():
    """
    :return: json array
    """
    user_input = request.args.get('input')
    print(user_input)
    dnn_result, result_bow = analyse.get_complete_result(user_input)
    print('RESULTDNN: ' + str(dnn_result))
    print('RESULTBOW: ' + str(result_bow))
    #TODO
    response = {
        'bow_url': ['<a href=\"' + i[0] + '\">' + i[0] + '</a>' for i in result_bow],
        'bow_value': [i[1] for i in result_bow],
        'dnn_result': dnn_result
    }
    return jsonify(response)



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")