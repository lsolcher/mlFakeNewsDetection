import numpy as np
import pickle
import tensorflow as tf
import pandas as pd
import collections

def save_obj(obj, path, name):
    with open(path + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path, name):
    with open(path + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def softmax(x):
    xt = np.exp(x - np.max(x))
    return xt / np.sum(xt)


def dict_to_list(dictio):
    the_list = []
    for value in dictio.values():
        the_list.append(value)
    return the_list


def lists_to_list_of_sentences(lists):
    one_list = []
    for item in lists:
        one_list += item
    return one_list


def lists_to_list_of_articles(lists):
    one_list = []

    for item in lists:
        one_list.append(''.join(map(str, item)))
    return one_list


def id_to_chars(chars):
    return {i: ch for i, ch in enumerate(chars)}


def build_vocab(filename):
  data = _read_words(filename)

  counter = collections.Counter(data)
  count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

  words, _ = list(zip(*count_pairs))
  word_to_id = dict(zip(words, range(len(words))))

  return word_to_id

def _read_words(filename):
  with tf.gfile.GFile(filename, "r") as f:
      return f.read().replace("\n", "<eos>").split()


def remove_duplicates(df):
    print('total size before removing duplicates: {}'.format(len(df.index)))
    # urls_to_remove = set()
    df['article_url'] = df['article_url'].str.replace('://m.', '://www.')
    df['article_url'] = df['article_url'].str.replace('://amp.', '://www.')
    df = df.drop_duplicates(subset='article_url')
    df = df.drop_duplicates(subset='article_text')

    """
    rows_to_check = df.loc[df['article_url'].str.contains('\?')]
    for index, row in rows_to_check.iterrows():
        url_to_check = row['article_url'].split('?')[0]
        possible_duplicates = df[df['article_url'].str.contains(url_to_check)]
        for entry in possible_duplicates:
            if entry['article_url'] != row['article_url'] and entry['article_text'] == row['article_tex']:
                urls_to_remove.append[entry['article_url']]

    df = [df['article_url'] != urls_to_remove]
                    """
    print('total size after removing duplicates: {}'.format(len(df.index)))
    return df

def get_df(predict_file):
    if type(predict_file) is dict:
        #for key, value in predict_file.items():
        #   print(key + ": " + str(value))
        #    print('\n')
        df = pd.DataFrame(dict([ (k, pd.Series(v)) for k, v in predict_file.items() ]))
        print(df)
        #df = df.dropna()
        #for index, row in df.iterrows():
        #    print(row['c1'], row['c2'])
        print(df)
    else:
        df = pd.read_csv(predict_file, sep='|')
    return df
