import os

CURRENTFOLDER = os.path.dirname(os.path.abspath(__file__))
DATAFOLDER = os.path.join(CURRENTFOLDER,'data/')
TWITTER_DATA_FILE = os.path.join(DATAFOLDER,'labeled_data.csv')
TEST_DATA_FILE = os.path.join(DATAFOLDER,'test.csv')
MODEL_FOLDER = os.path.join(DATAFOLDER,'models')
ARTICLE_TEXT_MODEL_FOLDER = os.path.join(DATAFOLDER,'obj/twitter/article_text/')
TWEET_TEXT_MODEL_FOLDER = os.path.join(DATAFOLDER,'obj/twitter/tweet_text/')
OBJECT_FOLDER = os.path.join(DATAFOLDER,'obj/')
ARTICLE_FOLDER = os.path.join(DATAFOLDER,'articles/')
BOW_FOLDER = os.path.join(DATAFOLDER,'bow/')

PROGRESSFILE = DATAFOLDER + '//progress.p' # scraper
PROGRESSFILE_BOW = BOW_FOLDER + '//progress.p'


asecret = 'Vy5hWwthlxuU6qSVoq91Bb4TjfJo9sHSrmx66BN04zoTX'
MIN_ARTICLE_LENGTH = 100
MIN_SENTENCE_LENGTH = 10
KEYWORDS_TO_TRACK = ['Hitler-Puppe', 'European Press Watch', 'altparteien', 'asyltourismus', 'zurücktreten', 'flüchtlinge', 'speigel', 'islamisierung'
                     'geheimvertrag', 'skandal', 'rücktritt', 'skandal', 'aufgedeckt', 'gudenus', 'merkel', 'gabriel', 'brexit', 'qanon', 'chemnitz', 'politik', 'bundesregierung', 'berliner express', 'krah', 'köthen', 'koethen']