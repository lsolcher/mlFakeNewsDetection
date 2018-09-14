import os
import nltk
import random
import pickle
from .utils import update_progress, get_progress
from ClassifierBasedGermanTagger import ClassifierBasedGermanTagger


def tag(tokens):
    tagger = os.path.join(os.path.dirname(__file__), "nltk_german_classifier_data.pickle")
    progress = get_progress()
    with open(tagger, 'rb') as f:
        ger_tagger = pickle.load(f)
    tagged_tokens = {}
    for idx, (key, t) in enumerate(tokens.items()):
        tagged_tokens[key] = ger_tagger.tag(t)
        if idx % 100 == 0:
            progress.append('{} von {} Artikeln getaggt!'.format(idx, len(tokens)))
            update_progress(progress)
    return tagged_tokens


def do_tag(tokens, tagger):
    tagged_tokens = []
    for t in tokens:
        tagged_tokens.append(tagger.tag(t))

    return tagged_tokens
