from .. import constants
from . import preprocessor
import time


def bow():

    counts, word_list, tokens = preprocessor.preprocess_tokens_per_document_from_csv()

    #BOW
    start = time.time()
    vocab = []
    for l in word_list:
        vocab.append(set())

    # for i, c in enumerate(counts):
    #   vocab[i] |= set(c.keys())

    # for v in vocab:
    #   v = sorted(list(v))  # sorting here only for better display later

    # bow = []s
    # for i, counter in enumerate(counts):
    #   bow_row = [counter.get(term, 0) for term in vocab[i]]
    #  bow.append(bow_row)
    resultfile = 'C:/Programmierung/Masterarbeit/Analyzer/results/results.csv'
    if not os.path.exists(resultfile):

        print('calculating similarities...')
        similarities = {}
        for i, c in counts.items():
            for j, c1 in counts.items():
                author1 = " ".join(re.findall("[a-zA-Z]+", i))
                author2 = " ".join(re.findall("[a-zA-Z]+", j))
                if author1 != author2 and i < j:
                    similarities[i + ' : ' + j] = counter_cosine_similarity(counts[i], counts[j])

        sorted_sims = sorted(similarities.items(), key=operator.itemgetter(1), reverse=True)
        end = time.time()
        print('done! took ', end - start, ' seconds.')

        with open(resultfile, 'w', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f)
            w.writerows(sorted_sims)
            
    return True