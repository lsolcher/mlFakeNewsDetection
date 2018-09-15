import time, traceback
from collections import Counter
import os, csv
from .. import constants
from . import utils, Tokenizer, Normalizer, Tagger, Lemmatizer
from .utils import update_progress


BOW_FOLDER = constants.BOW_FOLDER
test_string=''


def add_article_to_word_model(url, article):
    try:
        if not os.path.isfile(BOW_FOLDER + '/counts' + test_string + '.pkl') or \
            not os.path.isfile(BOW_FOLDER + '/word_list' + test_string + '.pkl') or  \
            not os.path.isfile(BOW_FOLDER + '/tokens' + test_string + '.pkl'):
            return 'Es sind keine Wortmodelle zu Artikeln vorhanden. Bitte diese zuerst erstellen.'
        else:
            progress = []
            start = time.time()
            print('tokenizing...')
            progress.append('Tokenisiere...')
            update_progress(progress)
            tokens = Tokenizer.tokenize_article(url, article)
            end = time.time()
            print('done! took ', end - start, ' seconds.')
            progress.append('Artikel tokenisiert in {} Sekunden!\n'.format(end-start))
            update_progress(progress)


            start = time.time()
            print('tagging...')
            progress.append('Tagge...')
            update_progress(progress)
            tokens = Tagger.tag(tokens)
            end = time.time()
            print('done! took ', end - start, ' seconds.')
            progress.append('Artikel getaggt in {} Sekunden!\n'.format(end-start))
            update_progress(progress)


            start = time.time()
            print('normalizing...')
            progress.append('Normalisiere...')
            update_progress(progress)
            tokens = Normalizer.normalize(tokens)
            end = time.time()
            print('done! took ', end - start, ' seconds.')
            progress.append('Artikel normalisiert in {} Sekunden!\n'.format(end-start))
            update_progress(progress)


            start = time.time()
            print('lemmatizing...')
            progress.append('Lemmatisiere...')
            update_progress(progress)
            tokens = Lemmatizer.lemmatize_tokens(tokens)
            end = time.time()
            print('done! took ', end - start, ' seconds.')
            progress.append('Artikel lemmatisiert in {} Sekunden!\n'.format(end-start))
            update_progress(progress)


            start = time.time()
            print('counting...')
            progress.append('Zähle...')
            update_progress(progress)


            word_list = {}
            for idx, token in tokens.items():
                word_list[idx] = ([t[0] for t in token])
            counts = {}
            for idx, item in word_list.items():
                counts[idx] = Counter(item)


            end = time.time()
            print('done! took ', end - start, ' seconds.')
            progress.append('Wörter gezählt in {} Sekunden!\n'.format(end-start))
            update_progress(progress)


            counts = utils.load_obj(BOW_FOLDER, 'counts', test_string)
            word_list = utils.load_obj(BOW_FOLDER, 'word_list', test_string)

            word_list[url] = ([t[0] for t in token])
            counts[url] = Counter(word_list[url])

            for idx, token in tokens.items():
                word_list[idx] = ([t[0] for t in token])
            for idx, item in word_list.items():
                counts[idx] = Counter(item)

            progress.append('BOW-Modell erstellt!')
            update_progress(progress)
            return word_list, counts
    except:
        traceback.print_exc()
        return None, None


def create_word_models_from_database():
    """
    Takes in a directory, parses the texts in each subdirectory and tokenizes each document
    :param direct:
    :param test_string: optional for testing
    :return:
    """
    try:
        # old_urls = get_old_urls()
        progress = []
        start = time.time()
        print('tokenizing...')
        progress.append('Tokenisiere...')
        update_progress(progress)

        old_urls = get_old_urls()

        tokens = Tokenizer.tokenize_from_dir_to_tokens_per_csv(old_urls)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        progress.append('Artikel tokenisiert in {} Sekunden!\n'.format(end-start))
        update_progress(progress)


        start = time.time()
        print('tagging...')
        progress.append('Tagge...')
        update_progress(progress)
        tokens = Tagger.tag(tokens)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        progress.append('Artikel getaggt in {} Sekunden!\n'.format(end-start))
        update_progress(progress)


        start = time.time()
        print('normalizing...')
        progress.append('Normalisiere...')
        update_progress(progress)
        tokens = Normalizer.normalize(tokens)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        progress.append('Artikel normalisiert in {} Sekunden!\n'.format(end-start))
        update_progress(progress)


        start = time.time()
        print('lemmatizing...')
        progress.append('Lemmatisiere...')
        update_progress(progress)
        tokens = Lemmatizer.lemmatize_tokens(tokens)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        progress.append('Artikel lemmatisiert in {} Sekunden!\n'.format(end-start))
        update_progress(progress)


        start = time.time()
        print('counting...')
        progress.append('Zähle...')
        update_progress(progress)
        word_list = {}
        for idx, token in tokens.items():
            word_list[idx] = ([t[0] for t in token])
        counts = {}
        for idx, item in word_list.items():
            counts[idx] = Counter(item)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        progress.append('Wörter gezählt in {} Sekunden!\n'.format(end-start))
        update_progress(progress)

        utils.save_obj(counts, BOW_FOLDER, 'counts', test_string)
        utils.save_obj(word_list, BOW_FOLDER, 'word_list', test_string)
        utils.save_obj(tokens, BOW_FOLDER, 'tokens', test_string)
        progress.append('BOW-Modell erstellt!')
        update_progress(progress)
        return 'Successfully created word models from database'
    except:
        traceback.print_exc()
        return 'An error occurred creating word models'


def get_old_urls():
    urls = []
    for file in os.listdir(BOW_FOLDER):
        if file.endswith(".txt") and '_urls' in file:
            with open(os.path.join(BOW_FOLDER, file), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()  # or some other preprocessing
                    urls.append(line)  # storing everything in memory!

    print(urls)
    return urls
"""
def has_sub_folder(path_to_parent):
    if type(path_to_parent) == list:
        for item in path_to_parent:
            if os.listdir(item):
                return True
    else:
        for fname in os.listdir(path_to_parent):
            if os.listdir(os.path.join(path_to_parent,fname)):
                return True
    return False


def get_immediate_subdirectories(a_dir):
    return [f.path for f in os.scandir(a_dir) if f.is_dir() ]


def preprocess_tokens_per_document(direct, test_string):

    Takes in a directory, parses the texts in each subdirectory and tokenizes each document
    :param direct:
    :return:
    
    if os.path.isfile(BOW_FOLDER + '/counts'+test_string+'.pkl') and \
        os.path.isfile(BOW_FOLDER + '/word_list'+test_string+'.pkl') and \
        os.path.isfile(BOW_FOLDER + '/tokens'+test_string+'.pkl'):
        counts = utils.load_obj(BOW_FOLDER, 'counts', test_string)
        word_list = utils.load_obj(BOW_FOLDER, 'word_list', test_string)
        tokens = utils.load_obj(BOW_FOLDER, 'tokens', test_string)
    else:
        start = time.time()
        print('tokenizing...')
        paths = direct
        tokens = Tokenizer.tokenize_from_dir_to_tokens_per_document(paths)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        start = time.time()

        print('tagging...')
        tokens = Tagger.tag(tokens)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        start = time.time()
        print('normalizing...')
        tokens = Normalizer.normalize(tokens)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        start = time.time()
        print('lemmatizing...')
        tokens = Lemmatizer.lemmatize_tokens(tokens)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        start = time.time()
        print('counting...')
        word_list = {}
        for idx, token in tokens.items():
            word_list[idx] = ([t[0] for t in token])
        counts = {}
        print('counting...')
        for idx, item in word_list.items():
            counts[idx] = Counter(item)
        end = time.time()
        print('done! took ', end - start, ' seconds.')
        utils.save_obj(counts, 'counts', test_string)
        utils.save_obj(word_list, 'word_list', test_string)
        utils.save_obj(tokens, 'tokens', test_string)
    return counts, word_list, tokens





def preprocess_tokens_per_source(direct, test_string):
    paths = []
    start = time.time()
    print('tokenizing...')
    if has_sub_folder(direct):
        paths = get_immediate_subdirectories(direct)
    else:
        paths = direct
    tokens = Tokenizer.tokenize_from_dir_to_tokens_per_source(paths)
    end = time.time()
    print('done! took ', end - start, ' seconds.')
    start = time.time()

    print('tagging...')
    tokens = Tagger.tag(tokens)
    end = time.time()
    print('done! took ', end - start, ' seconds.')
    start = time.time()
    print('normalizing...')
    tokens = Normalizer.normalize(tokens)
    end = time.time()
    print('done! took ', end - start, ' seconds.')
    start = time.time()
    print('lemmatizing...')
    tokens = Lemmatizer.lemmatize_tokens(tokens)
    end = time.time()
    print('done! took ', end - start, ' seconds.')
    start = time.time()
    print('counting...')
    word_list = {}
    for idx, token in tokens.items():
        word_list[idx] = ([t[0] for t in token])
    counts = {}
    print('counting...')
    for idx, item in word_list.items():
        counts[idx] = Counter(item)
        if idx % 100 == 0:
            print('counted {} of {} items'.format(idx, len(word_list.items())))
    end = time.time()
    print('done! took ', end - start, ' seconds.')
    save_obj(counts, 'counts_source'+test_string)
    save_obj(word_list, 'word_list_source'+test_string)
    save_obj(tokens, 'tokens_source'+test_string)
    return counts, word_list, tokens

def get_articles_from_top_dir(dirpath, test_string):
    start = time.time()
    print('getting text...')
    articles = {}
    if has_sub_folder(dirpath):
        paths = get_immediate_subdirectories(dirpath)
    else:
        paths = dirpath

    if type(paths) is list:
        for path in paths:
            text = ''
            for file in os.listdir(path):
                if file.endswith(".txt"):
                    text = open(os.path.join(path, file), encoding="utf8", errors='ignore').read()
                articles[file] = text
    else:
        for file in os.listdir(paths):
            text = ''
            if file.endswith(".txt"):
                text = open(os.path.join(dirpath, file), encoding="utf8", errors='ignore').read()
                articles[file] = text
    end = time.time()
    print('done! took ', end - start, ' seconds.')
    save_obj(articles, 'articles' + test_string)

    return articles
"""