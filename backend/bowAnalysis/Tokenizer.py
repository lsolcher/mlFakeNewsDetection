# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 18:11:24 2018

@author: Luc
"""
from .. import constants
import nltk
import os.path
import csv

ARTICLE_FOLDER = constants.ARTICLE_FOLDER


def tokenize_from_dir_to_tokens_per_csv(old_urls=None):
    tokens = {}
    for file in os.listdir(ARTICLE_FOLDER):
        if file.endswith(".csv"):
            with open(os.path.join(ARTICLE_FOLDER, file), 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter='|')
                for row in reader:
                    if not already_tokenized(row[0], old_urls):
                        tokens[row[0]] = nltk.word_tokenize(row[1], language='german')
    print(len(tokens))
    return tokens

def tokenize_article(url, article):
    tokens = {}
    print(article)
    tokens[url] = nltk.word_tokenize(article, language='german')
    return tokens


def already_tokenized(url_to_check, old_urls):
    print('URL' + url_to_check)

    if old_urls is None:
        print('1')
        return False
    else:
        if url_to_check in old_urls:
            print('2')
            return True
    print('3')
    return False

# def tokenize_from_dir_to_tokens_per_document(dirpath):
#     """
#     Takes in a list of directories or a single directory, reads in the text of all .txt in these dir(s) and tokenizes them
#     :param dirpath: a single directory or a list of directories
#     :return:
#     """
#
#     logger = logging.getLogger('root')
#     logger.info('start tokenization')
#
#     tokens = {}
#     if type(dirpath) is list:
#         for path in dirpath:
#             for file in os.listdir(path):
#                 if file.endswith(".txt"):
#                     text = open(os.path.join(path, file), encoding="utf8", errors='ignore').read()
#                     tokens[file] = nltk.word_tokenize(text, language='german')
#                 elif file.endswith(".csv"):
#                     df = pd.read_csv(os.path.join(path, file), sep='|')
#                     text_list = df['article_text'].tolist()
#                     label_list = df['article_url']
#                     for idx, item in enumerate(text_list):
#                         try:
#                             tokens[label_list[idx]] = nltk.word_tokenize(text_list[idx])
#                         except TypeError as e:
#                             print(e)
#     else:
#         for file in os.listdir(dirpath):
#             if file.endswith(".txt"):
#                 text = open(os.path.join(dirpath, file), encoding="utf8", errors='ignore').read()
#                 tokens[file] = nltk.word_tokenize(text, language='german')
#             elif file.endswith(".csv"):
#                 df = pd.read_csv(os.path.join(dirpath, file), sep='|')
#                 text_list = df['article_text'].tolist()
#                 label_list = df['article_url']
#                 for idx, item in enumerate(text_list):
#                     tokens[label_list[idx]] = nltk.word_tokenize(text_list[idx])
#
#     return tokens
#
# def tokenize_from_dir_to_tokens_per_source(dirpath):
#     """
#     Takes in a list of directories or a single directory, reads in the text of all .txt in these dir(s) and tokenizes them
#     :param dirpath: a single directory or a list of directories
#     :return:
#     """
#
#     logger = logging.getLogger('root')
#     logger.info('start tokenization')
#
#     tokens = {}
#     text = ''
#     if type(dirpath) is list:
#         for path in dirpath:
#             text = ''
#             for file in os.listdir(path):
#                 if file.endswith(".txt"):
#                     text += open(os.path.join(path, file), encoding="utf8", errors='ignore').read()
#             tokens[path] = nltk.word_tokenize(text, language='german')
#     else:
#         for file in os.listdir(dirpath):
#             text = ''
#             if file.endswith(".txt"):
#                 text += open(os.path.join(dirpath, file), encoding="utf8", errors='ignore').read()
#             tokens[file] = nltk.word_tokenize(text, language='german')
#
#     return tokens
#
#
# def tokenize_sentences(sentences):
#
#     logger = logging.getLogger('root')
#     logger.info('start tokenization')
#     if type(sentences) is dict:
#         tokens = {}
#         for key, item in sentences.items():
#             tokens[key] = [nltk.word_tokenize(sentence, language='german') for sentence in item]
#         return tokens
#     else:
#         return nltk.word_tokenize(sentences, language='german')






