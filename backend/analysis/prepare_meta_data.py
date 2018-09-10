import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import math
from . import utils


def create_train_test_from_twitter(data_file):
    df = pd.read_csv(data_file, sep='|', encoding='utf-8', keep_default_na=False)
    print('removing duplicates')
    df = utils.remove_duplicates(df)
    df = df.convert_objects(convert_numeric=True)
    #boolean_dictionary = {'True': 'TRUE', 'False': 'FALSE'} # replace boolean with int
    #df = df.replace(boolean_dictionary)
    df.verified = df.verified.astype(str).astype(bool).astype(int)
    print(df.dtypes)
    d = df.as_matrix(columns=['total_number_tweets', 'followers_count', 'friends_count', 'favourites_count', 'retweet_count', 'number_hashtags', 'number_quotes', 'verified']) # , 'number_replies', 'number_retweets'
    #TODO: verified, datecreated
    data = d.astype(np.float)
    for idx, item in enumerate(data):
        for idy, cell in enumerate(item):
            if math.isnan(cell):
                item[idy] = 0
    labels = np.vstack(df['is_fake'])
    y_train_ohe  = np.array([[1,0] if i==1 else [0,1] for i in labels])

    X_train, X_test, y_train, y_test = train_test_split(data, y_train_ohe, test_size=0.2)
    return X_train, X_test, y_train, y_test


def create_meta_data_from_twitter(data_file):
    df = utils.get_df(data_file)

    df = df.convert_objects(convert_numeric=True)
    #boolean_dictionary = {'True': 'TRUE', 'False': 'FALSE'} # replace boolean with int
    #df = df.replace(boolean_dictionary)
    df.verified = df.verified.astype(str).astype(bool).astype(int)
    print(df.dtypes)
    d = df.as_matrix(columns=['total_number_tweets', 'followers_count', 'friends_count', 'favourites_count', 'retweet_count', 'number_hashtags', 'number_retweets', 'verified']) # , 'number_quotes', 'number_replies's
    #TODO: verified, datecreated
    data = d.astype(np.float)
    for idx, item in enumerate(data):
        for idy, cell in enumerate(item):
            if math.isnan(cell):
                item[idy] = 0

    #labels = np.vstack(df['is_fake'])
    #y_train_ohe  = np.array([[1,0] if i==1 else [0,1] for i in labels])
    return data
