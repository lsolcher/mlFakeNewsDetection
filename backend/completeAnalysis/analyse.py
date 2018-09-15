from .. import tweet_analyzer
from ..dnnAnalysis import dnn_keras, utils
from ..bowAnalysis import bow


def get_complete_result(input_str):

    if input_str.isdigit():  # tweet-id
        success, result = tweet_analyzer.get_tweet_by_id(input_str)
        if success:
            result = dnn_keras.analyze_tweet(result)
            result_bow = bow.get_bow_result(result.article_text, process_url=False)
            print(result_bow)
            return utils.jsonify(result)
        else:
            # error string
            return result
    else:
        success, result = tweet_analyzer.get_tweet_by_url(input_str)
        if success:  # tweet-url
            result = dnn_keras.analyze_tweet(result)
            result_bow = bow.get_bow_result(result.article_text, process_url=False)
            print(result_bow)
            return utils.jsonify(result)
        else:
            success, result = tweet_analyzer.process_article(input_str)
            if success:
                print('im an article')
                result = dnn_keras.analyze_article(input_str, result)
                result_bow = bow.get_bow_result(input_str)
                print(result_bow)
                return utils.jsonify(result)
            else:
                # error string
                return result