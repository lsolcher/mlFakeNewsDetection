import tweepy
from bs4 import BeautifulSoup
import string
import re
from urllib.request import urlopen, HTTPError, Request
from urllib3.exceptions import ProtocolError
import requests
import pandas as pd
from langdetect import detect, lang_detect_exception
import traceback
import datetime
from backend import constants

ckey = 'rGxOFKgKRoGo1Kpl1FEqjNGlI'
csecret = 'nnk4mqbRdOQQsCy8rIwCAxHnFUO6iGgjkpSsM96bGSZcANg7mR'
atoken = '912478974-s9PU6WjEeZC0olc57moslUByXX7UeXxttrPH7YbK'


asecret = 'Vy5hWwthlxuU6qSVoq91Bb4TjfJo9sHSrmx66BN04zoTX'
MIN_ARTICLE_LENGTH = constants.MIN_ARTICLE_LENGTH
MIN_SENTENCE_LENGTH = constants.MIN_SENTENCE_LENGTH
KEYWORDS_TO_TRACK = constants.KEYWORDS_TO_TRACK
def get_tweet_by_id(tweet_id):
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        tweet = api.get_status(tweet_id)
        success, respond = process_tweet(tweet)
        return success, respond
    except tweepy.TweepError as e:
        print(traceback.format_exc())
        return False, 'The entered tweet id does not exist.'


def get_tweet_by_url(tweet_url):
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        tweet = api.get_status(tweet_url.split('/')[-1])
        success, respond = process_tweet(tweet)
        return success, respond
    except tweepy.TweepError as e:
        print(traceback.format_exc())
        return False, 'The entered tweet id does not exist.'


def get_article_url(url):
    resp = urlopen(url)
    soup = BeautifulSoup(resp, 'html.parser', from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        if '/t.co/' in link['href']:
            r = requests.get(link['href'])
            url = r.url
            print('THISURL: ' + url)
            if '//twitter.com/' not in url:
                return url
    return None


def process_article(url_input):
    try:
        r = requests.get(url_input)
        url = r.url  # twitter is redircecting - get the correct link
        if url is not None:
            all_text, all_hidden_text, article = is_article(url, check_for_duplicates=False)
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
        return False, 'Die Eingabe scheint weder eine Twitter-Id noch eine URL zu sein.'


def process_tweet(status):
    print('STATUS:')
    print(status)
    print('\n\n\n')

    try:
        if hasattr(status, 'retweeted_status'):
            try:
                tweet = status.retweeted_status.extended_tweet["full_text"]
            except:
                tweet = status.retweeted_status.text
        else:
            try:
                tweet = status.extended_tweet["full_text"]
            except AttributeError:
                tweet = status.text
        urls = re.findall(r"http\S+", tweet)
        #print(tweet)
        print('URLS: ')
        for u in urls:
            print(u)
        if urls:
            try:
                print(tweet)
                print(urls)
                print('------------')
                for idx, url_input in enumerate(urls):
                    r = requests.get(url_input)
                    url = r.url  # twitter is redircecting - get the correct link
                    print('URL_INPUT: ' + url)
                    if 'twitter.com/i/' in url:
                        url = get_article_url(url)
                    if url is not None:
                        all_text, all_hidden_text, article = is_article(url, check_for_duplicates=False)

                        #  format text to not mess up csv writing
                        all_text = all_text.replace('|', ';')  # we use | as csv delimiter so replace them
                        all_hidden_text = all_hidden_text.replace('|', ';')
                        all_hidden_text = all_hidden_text.replace('\n', ' ')
                        all_text = all_text.replace('\n', ' ')
                        tweet = tweet.replace('\n', ' ')
                        all_hidden_text = all_hidden_text.replace('\r', ' ')
                        all_hidden_text = all_hidden_text.replace('\t', ' ')
                        all_hidden_text = all_hidden_text.replace('  ', ' ')
                        all_text = all_text.replace('\r', ' ')
                        tweet = tweet.replace('\r', ' ')
                        all_text = all_text.rstrip()
                        all_hidden_text = all_hidden_text.rstrip()
                        tweet = tweet.replace('|', ';')

                        print('{}: Found Tweet with links'.format(datetime.datetime.now().time()))
                        if article:
                            tweet_url = 'https://twitter.com/i/web/status/' + str(status.id)  # twitter url to retireve ids
                            if hasattr(status, 'retweeted_status'):  # tweet is retweet
                                print('Tweet is retweet, getting original tweet')
                                fields = {}
                                fields['tweet_url'] = tweet_url
                                fields['article_url'] = url
                                fields['article_text'] = all_text
                                fields['tweet_id'] = status.retweeted_status.id_str
                                fields['user_id'] = status.retweeted_status.author.id_str
                                fields['user_str'] = status.retweeted_status.author.screen_name
                                fields['account_created'] = status.retweeted_status.author.created_at
                                fields['total_number_tweets'] = status.retweeted_status.author.statuses_count
                                fields['followers_count'] = status.retweeted_status.author.followers_count
                                fields['friends_count'] = status.retweeted_status.author.friends_count
                                fields['favourites_count'] = status.retweeted_status.author.favourites_count
                                fields['verified'] = status.retweeted_status.author.verified
                                fields['retweet_count'] = status.retweeted_status.retweet_count
                                fields['number_hashtags'] = len(status.retweeted_status.entities.get('hashtags'))
                                fields['hashtags'] = status.retweeted_status.entities.get('hashtags')
                                fields['number_urls'] =  len(status.retweeted_status.entities.get('urls'))
                                fields['urls_str'] = status.retweeted_status.entities.get('urls')
                                fields['tweet_text'] = tweet
                                fields['timestamp'] = status.retweeted_status.created_at
                                #TODO
                                fields['number_quotes'] = 0# status.retweeted_status.quote_count
                                fields['number_replies'] = 0# status.retweeted_status.reply_count
                                fields['number_retweets'] = 0# status.retweeted_status.retweet_count
                                fields['skipped_text'] = all_hidden_text
                            else:  # tweet is original tweet
                                print('Tweet is original tweet')
                                fields = {}
                                fields['tweet_url'] = tweet_url
                                fields['article_url'] = url
                                fields['article_text'] = all_text
                                fields['tweet_id'] = status.id_str
                                fields['user_id'] = status.author.id_str
                                fields['user_str'] = status.author.screen_name
                                fields['account_created'] = status.author.created_at
                                fields['total_number_tweets'] = status.author.statuses_count
                                fields['followers_count'] = status.author.followers_count
                                fields['friends_count'] = status.author.friends_count
                                fields['favourites_count'] = status.author.favourites_count
                                fields['verified'] = status.author.verified
                                fields['retweet_count'] = status.retweet_count
                                fields['number_hashtags'] =  len(status.entities.get('hashtags'))
                                fields['hashtags'] = status.entities.get('hashtags')
                                fields['number_urls'] = len(status.entities.get('urls'))
                                fields['urls_str'] = status.entities.get('urls')
                                fields['tweet_text'] = tweet
                                fields['timestamp'] = status.created_at
                                fields['number_quotes'] = 0
                                fields['number_replies'] = 0
                                fields['number_retweets'] = 0
                                fields['skipped_text'] = all_hidden_text
                            return True, fields
                            # try:
                            #     with open(constants.TWITTER_DATA_FILE, 'a', encoding='utf-8', newline='') as f:
                            #         writer = csv.writer(f, delimiter='|')
                            #         writer.writerow(fields)
                            #     print('Wrote linked article(s) from {}'.format(url))
                            # except:
                            #     print('Resultfile open, Couldn\'t write article from {}'.format(url))
                        else:
                            return False, '{} verlinkt auf keinen Artikel'.format(url)
                    else:
                        return False, 'Konnte keine Artikel in {} finden.'.format(url)
            except Exception as e1:
                print('Unexpected Exception')
                print(traceback.format_exc())
                return False, 'Could not process tweet'
    except ProtocolError as e2:
        return False, 'Catched error: {}'.format(e2)

def is_article(url, check_for_duplicates=True):
    try:
        # check duplicates
        df = pd.read_csv(constants.TWITTER_DATA_FILE, sep='|', header=0)

        if '://m.' in url:
            url.replace('://m.', '://www.')

        if '://amp.' in url:
            url.replace('://amp.', '://www.')

        if check_for_duplicates:
            if "article_url" in df.columns:
                #  TODO: check if article after ? is the same
                articles = df['article_url'].tolist()
                #print(df['article_url'].unique())
                if url in articles:  # ie we already found this article
                    # TODO: increment times found
                    print('{} already in list'.format(url))
                    return '', '', False

        # check url for duplicates, not-article-pages etc
        checkurl = url
        if not checkurl.endswith('/'):
            checkurl += '/'
        if 'twitter.com' in url or "wikipedia" in url or 'youtube' in url or 'change.org' in url or 'amazon' in checkurl \
                or checkurl.count('/') < 4:
            # we don't want another tweet or wiki entry, we want articles
            # if \ less than three we probably have a home dir
            print('{} seems not to be an article page'.format(url))
            return '', '', False


        req = Request(url, headers={'User-Agent': "Magic Browser"})  # to prevent 403 - forbidden
        #req = req.rstrip('\\')
        page = urlopen(req).read()

        # get text
        all_text, all_hidden_text = text_from_html(page)


        # make sure we get no duplicates because of url with different strings after ? referncing to the same page
        if '?' in checkurl:
            url_string = checkurl.split('?')[0]
            rows = df.loc[df['article_url'].str.contains(url_string)]
            if all_text in rows.article_text:  # ie we already found this article
                print('{} already in list'.format(checkurl))
                return '', '', False


        # check language
        if all_text is None:  # if there is no text, it's obviously no article
            return '', '', False
        try:
            lang = detect(all_text)
        except lang_detect_exception.LangDetectException as e:
            print('Language detection error for url {}'.format(url))
            print(e)
            return '', '', False
        if lang != 'de':  # we only want german articles
            print('Language is not German')
            return all_text, all_hidden_text, False

        # check nr words
        number_words = sum([i.strip(string.punctuation).isalpha() for i in all_text.split()])
        print('{} has {} words'.format(url, number_words))
        if number_words > MIN_ARTICLE_LENGTH:  # if it has less than 200 words, it's most likely no article
            return all_text, all_hidden_text, True  # we found an article
        return all_text, '', False
    except AttributeError as e:
        print('Attribute error parsing {}'.format(url))
        print(str(e))
        return '', '', False
    except HTTPError as e:
        print('HTTPError error parsing {}'.format(url))
        print(str(e))
        traceback.print_exc()
        return '', '', False


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
