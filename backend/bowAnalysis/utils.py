import pickle, requests, traceback
from bs4 import BeautifulSoup
from .. import constants
from urllib.request import urlopen, HTTPError, Request
from langdetect import detect, lang_detect_exception
import string, re, datetime
from shutil import copyfile
import os

MIN_ARTICLE_LENGTH = constants.MIN_ARTICLE_LENGTH
MIN_SENTENCE_LENGTH = constants.MIN_SENTENCE_LENGTH

def save_obj(obj, path, name, test_string = ''):
    with open(path + name + test_string + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path, name, test_string=''):
    with open(path + name + test_string + '.pkl', 'rb') as f:
        return pickle.load(f)

def update_progress(data):
    with open(constants.PROGRESSFILE_BOW, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)

def get_progress():
    with open(constants.PROGRESSFILE_BOW, 'rb') as fp:
        progress = pickle.load(fp)
    return progress


def process_article(url_input):
    try:
        r = requests.get(url_input)
        url = r.url  # twitter is redircecting - get the correct link
        if url is not None:
            all_text, article = is_article(url)
            #  format text to not mess up csv writing
            all_text = all_text.replace('|', ';')  # we use | as csv delimiter so replace them
            all_text = all_text.replace('\n', ' ')
            all_text = all_text.replace('\r', ' ')
            all_text = all_text.rstrip()
            print('{}: Found Tweet with links'.format(datetime.datetime.now().time()))
            if article:
                return True, all_text
            else:
                return False, '{} verlinkt auf keinen Artikel'.format(url)
        else:
            return False, 'Konnte keine Artikel in {} finden.'.format(url)
    except:
        traceback.print_exc()
        return False, 'Die Eingabe scheint weder eine Twitter-Id noch eine URL zu sein.'


def is_article(url):
    try:
        req = Request(url, headers={'User-Agent': "Magic Browser"})  # to prevent 403 - forbidden
        #req = req.rstrip('\\')
        page = urlopen(req).read()

        # get text
        all_text, all_hidden_text = text_from_html(page)
        # check language
        if all_text is None:  # if there is no text, it's obviously no article
            return '', False
        try:
            lang = detect(all_text)
        except lang_detect_exception.LangDetectException as e:
            print('Language detection error for url {}'.format(url))
            print(e)
            return '', False
        if lang != 'de':  # we only want german articles
            print('Language is not German')
            return all_text, False

        # check nr words
        number_words = sum([i.strip(string.punctuation).isalpha() for i in all_text.split()])
        print('{} has {} words'.format(url, number_words))
        if number_words > MIN_ARTICLE_LENGTH:  # if it has less than 200 words, it's most likely no article
            return all_text, True  # we found an article
        return all_text, False
    except AttributeError as e:
        print('Attribute error parsing {}'.format(url))
        print(str(e))
        return '', False
    except HTTPError as e:
        print('HTTPError error parsing {}'.format(url))
        print(str(e))
        traceback.print_exc()
        return '', False


def text_from_html(body):
    # TODO
    soup = BeautifulSoup(body, 'html.parser')
    page = soup.find_all('p')
    all_text = ''
    all_hidden_text = ''
    max_number_words = 0
    for p in page:  # get all p-tag-texts
        # check for hidden elements such as comments
        hidden, hidden_text = element_is_hidden(p)
        all_hidden_text += xstr(hidden_text)
        if not hidden:
            # TODO: get hidden text
            text = p.get_text()
            number_words = sum([i.strip(string.punctuation).isalpha() for i in text.split()])
            regex_html = re.compile(r'<\\*>')
            regex_space = re.compile(r' {3,100}')
            regex_newline = re.compile(r'\n{3,100}')
            if regex_html.search(text):
                print('Text contains html elements: \n\n {}'.format(text))
            try:
                # ignore all <p> with unusual elements
                if number_words > 5 and '\n\n' not in text \
                        and 'kein Javascript' not in text\
                        and '\t\t' not in text \
                        and not regex_html.search(text) \
                        and not regex_space.search(text) \
                        and not regex_newline.search(text) \
                        and not text.endswith('…') \
                        and 'Images' not in text \
                        and 'Adblocker' not in text \
                        and 'Cookie-Einstellungen' not in text \
                        and 'Suche ergab keinen Treffer' not in text \
                        and ('id' not in p.attrs or ('id' in p.attrs and 'ua-hint' not in p.attrs['id'])):
                    # and "  " not in text -- maybe
                    # TODO: get zeit articles
                    sentences = re.split(r'[\n.]+', text)  # get the single sentences
                    for s in sentences:
                        if re.match('\W*mehr\W*', s):  # this is usually a teaser text
                            print('Seems like a teaser or mainpage: {}'.format(text))
                            return '', ''

                        #  get the longest sentence - needed to determine if it is an article
                        number_words_in_sent = sum([i.strip(string.punctuation).isalpha() for i in s.split()])
                        if max_number_words < number_words_in_sent:
                            max_number_words = number_words_in_sent
                    # we probably have an article paragraph
                    all_text += text
                else:
                    print('Unusual text piece, skipping: {}'.format(text))
            except Exception as ex:
                print('Error parsing text data from {}'.format(page))
                print(traceback.format_exc())

    if max_number_words < MIN_SENTENCE_LENGTH:
        print('No sentence in {} longer than {} words. That\'s highly unlikely an article'.format(page, MIN_SENTENCE_LENGTH))
        return '', ''
    while all_text.endswith(' '):
        all_text = all_text[:-1]
    return all_text, all_hidden_text


def element_is_hidden(p):
    """
    check all the parents of an element and the element itsself for ids and classes which typically mark hidden elements
    - ie comments, popups, donation requests etc.
    :param p: the element to check
    :return: True, hidden_text: if the element is hidden return true and the hidden text
             False, '': if the element is not hidden return false
    """
    # TODO: https://www.afd.de/georg-pazderski-ohnmaechtiger-staat-laesst-polizisten-im-stich/ -- footer?
    if 'class' in p.attrs:
        for text in p['class']:
            if 'advert' in text or 'copyright' in text:
                print('Seems like a hidden or irrelevant entry: {}'.format(p.get_text()))
                return True, p.get_text()
    if 'id' in p.attrs:
        for text in p['id']:
            if 'advert' in text or 'copyright' in text:
                print('Seems like a hidden or irrelevant entry: {}'.format(p.get_text()))
                return True, p.get_text()
    has_parent = True
    while has_parent:
        if p.parent is not None:
            parent = p.parent
            if 'class' in parent.attrs:
                for text in parent['class']:
                    if 'teaser' in text or \
                            'footer' in text or \
                            'comment' in text or \
                            'donation' in text or \
                            'pop-up' in text or \
                            'login' in text or \
                            'header' in text:
                        print('Seems like a hidden or irrelevant entry: {}'.format(p.get_text()))
                        return True, p.get_text()
            if 'id' in parent.attrs:
                for text in parent['id']:
                    if 'teaser' in text or \
                            'footer' in text or \
                            'comment' in text or \
                            'donation' in text or \
                            'pop-up' in text or \
                            'login' in text or \
                            'header' in text:
                        print('Seems like a hidden or irrelevant entry: {}'.format(p.get_text()))
                        return True, p.get_text()
            p = p.parent
        else:
            has_parent = False
    return False, None


def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)


def save_used_urls():
    for file in os.listdir(constants.ARTICLE_FOLDER):
        if file.endswith(".txt") and '_urls' in file:
            copyfile(os.path.join(constants.ARTICLE_FOLDER, file), os.path.join(constants.BOW_FOLDER, file))

