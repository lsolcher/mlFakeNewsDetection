# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 19:24:10 2018

@author: Luc
"""
import nltk
import itertools


def normalize(tokens):
    
    print(len(tokens))
    new_tokens = {}

    for idx, t in tokens.items():
        print(len(t))
        t = remove_special_chars(t)
        print(len(t))
        t = remove_stopwords(t)
        print(len(t))
        #t = stem(t)
        #print(len(t))
        # correct spelling
        new_tokens[idx] = t

    print("done")
    return new_tokens

    
def remove_stopwords(token):

    new_token = []
    stopwords = nltk.corpus.stopwords.words('german')
    for t in token:
        if t[0].lower() not in stopwords:
            new_token.append(t)
    return new_token


def remove_special_chars(token):

    new_token = []
    for t in token:
        if t[0].isalpha():
            new_token.append(t)
    return new_token


def stem(token):

    stemmer = nltk.stem.SnowballStemmer('german')
    new_token = []
    for t in token:
        new_token.append(tuple(stemmer.stem(t[0]), t[1]))
        #print(t)
    return new_token


def remove_uncommon_words_and_index_sentences(tokens, vocabulary_size, unknown_token):
    """
    Take a dictionary of tokens, get all sentences from it (while removing the keys) count the words and replace the
    least frequent words with a specified token to reach a total unique word count as specified with vocabulary size
    :param tokens:
    :param vocabulary_size:
    :param unknown_token:
    :return: A list with all sentences where all unfrequent words are replaced with the unknown_token
    """
    all_sentences = []
    for item in tokens.values():
        all_sentences += item
    word_freq = nltk.FreqDist(itertools.chain(*all_sentences))
    print("Found %d unique words tokens." % len(word_freq.items()))
    vocab = word_freq.most_common(vocabulary_size - 1)
    index_to_word = [x[0] for x in vocab]
    index_to_word.append(unknown_token)
    word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])
    print("Using vocabulary size %d." % vocabulary_size)
    print("The least frequent word in our vocabulary is '%s' and appeared %d times." % (vocab[-1][0], vocab[-1][1]))
    for i, sent in enumerate(all_sentences):
        all_sentences[i] = [w if w in word_to_index else unknown_token for w in sent]
    return all_sentences, word_to_index, index_to_word


def set_start_and_end_flags(sentences, sentence_start_token, sentence_end_token):
    new_sentences = {}
    total_count = 0
    for key, item in sentences.items():
        new_sentences[key] = ["%s %s %s" % (sentence_start_token, x, sentence_end_token) for x in item]
        total_count += len(new_sentences[key])
    print("Parsed %d sentences." % total_count)
    return new_sentences
