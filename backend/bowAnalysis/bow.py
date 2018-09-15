from .. import constants
from . import preprocessor, utils
import time, math, operator, csv, os
from pathlib import Path

BOW_FOLDER = constants.BOW_FOLDER
test_string = ''

def create_bow_model():
    prepare_progress_file()
    result = preprocessor.create_word_models_from_database()
    utils.save_used_urls()
    return result



def get_bow_result(input_str, process_url=True):
    success, article_text = utils.process_article(input_str)
    word_list, counts = preprocessor.add_article_to_word_model(input_str, article_text)
    if word_list is None or counts is None:
        return 'Ein unerwarteter Fehler beim Erstellen des BOW-Modells ist aufgetreten'
    prepare_result_file()
    #
    # BOW
    start = time.time()
    # vocab = []
    # for l in word_list:
    #    vocab.append(set())

    # for i, c in enumerate(counts):
    #   vocab[i] |= set(c.keys())

    # for v in vocab:
    #   v = sorted(list(v))  # sorting here only for better display later

    # bow = []s
    # for i, counter in enumerate(counts):
    #   bow_row = [counter.get(term, 0) for term in vocab[i]]
    #  bow.append(bow_row)


    print('calculating similarities...')
    similarities = {}
    for i, c in counts.items():
        if i != input_str:
            similarities[i] = counter_cosine_similarity(counts[i], counts[input_str])

    sorted_sims = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
    end = time.time()
    print('done! took ', end - start, ' seconds.')

    with open(constants.RESULTFILE_BOW, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerows(sorted_sims)

    return sorted_sims[:10]


def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


def prepare_result_file():
    Path(constants.RESULTFILE_BOW).touch(exist_ok=True)
    with open(constants.RESULTFILE_BOW, "w"):
        pass


def prepare_progress_file():
    if not os.path.exists(constants.BOW_FOLDER):
        os.makedirs(constants.BOW_FOLDER)
    Path(constants.PROGRESSFILE_BOW).touch(exist_ok=True)
    with open(constants.PROGRESSFILE_BOW, "w"):
        pass