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

PROGRESSFILE = DATAFOLDER + '//progress.p'
