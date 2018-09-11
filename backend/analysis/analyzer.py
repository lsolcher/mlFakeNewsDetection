from . import dnn_keras, utils, tweet_analyzer


def analyze_input(input_str):

    if input_str.isdigit():  # tweet-id
        success, result = tweet_analyzer.get_tweet_by_id(input_str)
        if success:
            result = dnn_keras.analyze_tweet(result)
            return utils.jsonify(result)
        else:
            # error string
            return result
    else:
        success, result = tweet_analyzer.get_tweet_by_url(input_str)
        if success:  # tweet-url
            result = dnn_keras.analyze_tweet(result)
            return utils.jsonify(result)
        else:
            success, result = tweet_analyzer.process_article(input_str)
            if success:
                result = dnn_keras.analyze_article(input_str, result)
                return utils.jsonify(result)
            else:
                # error string
                return result

"""
def run():
    # logger
    per_source = True
    datapath = os.path.abspath(os.path.dirname(__file__)) + '\\data\\'
    logger = log.setup_custom_logger('root')
    logger.info('start analyzing')
    main_path = 'C:\\Programmierung\\Masterarbeit\\Scraper\\data\\articles\\'
    test_path = 'C:/Programmierung/Masterarbeit/Scraper/data/test'
    valid_path = 'C:/Programmierung/Masterarbeit/Scraper/data/valid'
    model_path = 'C:/Programmierung/Masterarbeit/Analyzer/data/trainedModels'

    # dirs_to_train = load_dirs(main_path)

    # counts, word_list, tokens = prepare_data(main_path, per_source, '')
    # counts_test, word_list_test, tokens_test = prepare_data(test_path, per_source, '_test')
    # counts_valid, word_list_valid, tokens_valid = prepare_data(valid_path, per_source, '_valid')
    if os.path.isfile(constants.DATAFOLDER + '/obj/articles.pkl'):
        articles = utils.load_obj(constants.DATAFOLDER, 'articles')
    else:
        articles = preprocessor.get_articles_from_top_dir(main_path, '')
    if os.path.isfile(constants.DATAFOLDER + '/obj/articles_test.pkl'):
        articles_test = utils.load_obj('articles_test')
    else:
        articles_test = preprocessor.get_articles_from_top_dir(test_path, '_test')

    print('starting analysis')
    # cnn_model.train()
    # rnn_tensorflow.run(articles, articles_test)
    # rnn_eval.run(articles_test)
    # bow(main_path)
    dnn_keras.run(articles, articles_test, True)
"""