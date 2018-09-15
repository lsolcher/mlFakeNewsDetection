from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from backend.dnnAnalysis import analyzer
from backend.scraping import scraper
from backend.bowAnalysis import bow
from backend.completeAnalysis import analyse
from backend import constants
import requests, time, threading, datetime
import pickle

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.debug = False
CORS(app)
start_runner()


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            now = datetime.datetime.now()
            print(now.hour)
            if now.hour == 23 and now.minute == 59:
                scrape()
                createBow()
                print('updated models')
            print("Run recurring task")
            time.sleep(59)

    thread = threading.Thread(target=run_job)
    thread.start()


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
    print('DONE')
    response = {
        'result': result
    }
    return jsonify(response)

@app.route('/api/scrape_progress')
def scrape_progress():
    with open(constants.PROGRESSFILE_SCRAPER, 'rb') as fp:
        progress = pickle.load(fp)
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