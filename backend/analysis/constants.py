import os

CURRENTFOLDER = os.path.dirname(os.path.abspath(__file__))
TOPFOLDER = os.path.abspath(os.path.join(CURRENTFOLDER, os.pardir))
DATAFOLDER = os.path.join(TOPFOLDER,'data/')
TWITTER_DATA_FILE = os.path.join(DATAFOLDER,'labeled_data.csv')
TEST_DATA_FILE = os.path.join(DATAFOLDER,'test.csv')
MODEL_FOLDER = os.path.join(DATAFOLDER,'models')
ARTICLE_TEXT_MODEL_FOLDER = os.path.join(DATAFOLDER,'obj/twitter/article_text/')
TWEET_TEXT_MODEL_FOLDER = os.path.join(DATAFOLDER,'obj/twitter/tweet_text/')