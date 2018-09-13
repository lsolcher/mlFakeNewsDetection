import os
import nltk
import random
import pickle
from ClassifierBasedGermanTagger import ClassifierBasedGermanTagger


def tag(tokens):
    tagger = os.path.join(os.path.dirname(__file__), "nltk_german_classifier_data.pickle")

    with open(tagger, 'rb') as f:
        ger_tagger = pickle.load(f)
    tagged_tokens = {}
    for idx, t in tokens.items():
        tagged_tokens[idx] = ger_tagger.tag(t)
        print("tagged ", idx)
    return tagged_tokens


def do_tag(tokens, tagger):
    tagged_tokens = []
    for t in tokens:
        tagged_tokens.append(tagger.tag(t))

    return tagged_tokens
