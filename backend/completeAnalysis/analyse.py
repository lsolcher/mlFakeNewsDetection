from .. import tweet_analyzer
from ..dnnAnalysis import dnn_keras, utils
from ..bowAnalysis import bow


def get_complete_result(input_str):
    if input_str.isdigit():  # tweet-id
        success, result = tweet_analyzer.get_tweet_by_id(input_str)
        if success:
            dnn_result = dnn_keras.analyze_tweet(result)
            result_bow = bow.get_bow_result(result['article_text'], process_url=False)
            return utils.jsonify(dnn_result), utils.jsonify(result_bow)
        else:
            # error string
            return result, ''
    else:
        success, result = tweet_analyzer.get_tweet_by_url(input_str)
        if success:  # tweet-url
            dnn_result = dnn_keras.analyze_tweet(result)
            result_bow = bow.get_bow_result(result['article_text'], process_url=False)
            return utils.jsonify(dnn_result), utils.jsonify(result_bow)
        else:
            success, result = tweet_analyzer.process_article(input_str)
            if success:
                dnn_result = dnn_keras.analyze_article(input_str, result)
                result_bow = bow.get_bow_result(input_str)
                return utils.jsonify(dnn_result), utils.jsonify(result_bow)
            else:
                # error string
                return result, ''