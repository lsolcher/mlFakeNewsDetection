import spacy
import re
from stop_words import get_stop_words
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import label_binarize
from sklearn.model_selection import train_test_split
from gensim.models.word2vec import Word2Vec
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import gensim
import os
from . import utils

PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-.?!;:\"()äöüßÄÖÜ% "

def save_obj(obj, name ):
    with open('data/obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('data/obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)



def get_spacy_corpus(articles, nlp, logging=False, topic_modelling=False):
    texts = []
    counter = 1
    for source in articles:
        if counter % 100 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(articles)))
        counter += 1
        source = get_preprocessed_text(source)
        doc = nlp(source.lower())
        """
        # POS-Tagging
        for token in docjf:
            print(token.text, token.pos_, token.tag_)
        # NER-Tagging
        for token in docjf:
            print(token.text, token.ent_type_)
        for ent in docjf.ents:
            print(ent.text, ent.label_)
        """
        # we add some words to the stop word list
        article = []
        for w in doc:
            # if it's not a stop word or punctuation mark, add it to our article!
            if w.text != '\n' and not w.is_stop and not w.is_punct and not w.like_num:
                # we add the lematized version of the word
                article.append(w.lemma_)
            # if it's a new line, it means we're onto our next document
            if topic_modelling and w.text == '\n':
                texts.append(article)
                article = []
        if not topic_modelling:
            texts.append(' '.join(article))
    return pd.Series(texts)


# Define function to preprocess text for a word2vec model
def cleanup_text_word2vec(docs, nlp, logging=False):
    sentences = []
    counter = 1
    for doc in docs:
        if counter % 100 == 0 and logging:
            print("Processed %d out of %d documents" % (counter, len(docs)))

        doc = get_preprocessed_text(doc)
        # Disable tagger so that lemma_ of personal pronouns (I, me, etc) don't getted marked as "-PRON-"
        doc = nlp(doc, disable=['tagger'])
        # Grab lemmatized form of words and make lowercase
        doc = " ".join([tok.lemma_.lower() for tok in doc])
        # Split into sentences based on punctuation
        doc = re.split("[\.?!;] ", doc)
        # Remove commas, periods, and other punctuation (mostly commas)
        doc = [re.sub("[\.,;:!?]", "", sent) for sent in doc]
        # Split into words
        doc = [sent.split() for sent in doc]
        sentences += doc
        counter += 1
    return sentences

def get_preprocessed_text(text):
    text = "".join(c for c in text if c in PERMITTED_CHARS) # remove not permitted chars
    text = re.sub(' +', ' ', text) # remove multiple spaces
    final = re.sub("\n|\r", "", text)
    final += '\n' # to mark it as and of file
    return final


# Define function to create word vectors given a cleaned piece of text.
def create_average_vec(doc, wordvec_model):
    text_dim = 300
    average = np.zeros((text_dim,), dtype='float32')
    num_words = 0.
    for word in doc.split():
        if word in wordvec_model.wv.vocab:
            average = np.add(average, wordvec_model[word])
            num_words += 1.
    if num_words != 0.:
        average = np.divide(average, num_words)
    return average


def prepare_twitter_data(data_file, type_of_analysis):
    labels = []
    text_fake, text_normal = '', ''
    df = pd.read_csv(data_file, sep='|', encoding='utf-8', keep_default_na=False)
    print('removing duplicates')
    df = utils.remove_duplicates(df)
    print('getting preprocessed train articles')
    idx = 0
    for key, item in enumerate(df['article_text']):
        idx += 1
        if df['is_fake'].values[key] == 1:
            text_fake += get_preprocessed_text(item)
            labels.append('FAKE')
        else:
            text_normal += get_preprocessed_text(item)
            labels.append('NOT_FAKE')
        if idx % 100 == 0:
            print('got {} of {} preprocessed train articles'.format(idx, len(df)))

    print('Finished gathering train text items')

    train = pd.DataFrame()
    train['data'] = df[type_of_analysis]
    train['labels'] = df['is_fake']


    #  TOPIC MODELLING
    nlp = spacy.load("de")
    stop_words = get_stop_words('de')
    stop_words.append('foto')
    stop_words.append('⬅')

    for stopword in stop_words:
        lexeme = nlp.vocab[stopword]
        lexeme.is_stop = True

    texts = get_spacy_corpus(train['data'], nlp, logging=True, topic_modelling=True)
    bigram = gensim.models.Phrases(texts)
    texts = [bigram[line] for line in texts]
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    ldamodel = LdaModel(corpus=corpus, num_topics=10, id2word=dictionary)
    print(ldamodel.show_topics())
    return do_create_twitter(train, None)

def prepare_scraped_data(train_docs, test_docs):
    labels = []
    text_jf, text_spon, text_zeit = '', '', ''

    print('getting preprocessed train articles')
    idx = 0
    for key, item in train_docs.items():
        idx += 1
        if 'JF' in key:
            text_jf += get_preprocessed_text(item)
            labels.append('JF')
        elif 'SPON' in key:
            text_spon += get_preprocessed_text(item)
            labels.append('SPON')
        elif 'SZ' in key:
            text_zeit += get_preprocessed_text(item)
            labels.append('SZ')
        if idx % 100 == 0:
            print('got {} of {} preprocessed train articles'.format(idx, len(train_docs.items())))

    print('Finished gathering train text items')

    train = pd.DataFrame()
    train['data'] = list(train_docs.values())
    train['labels'] = labels

    labels_test = []
    print('getting preprocessed test articles')
    idx = 0
    for key, item in test_docs.items():
        idx += 1
        if 'JF' in key:
            text_jf += get_preprocessed_text(item)
            labels_test.append('JF')
        elif 'SPON' in key:
            text_spon += get_preprocessed_text(item)
            labels_test.append('SPON')
        elif 'SZ' in key:
            text_zeit += get_preprocessed_text(item)
            labels_test.append('SZ')
        if idx % 100 == 0:
            print('got {} of {} preprocessed train articles'.format(idx, len(test_docs.items())))

    print('Finished gathering test text items')
    test = pd.DataFrame()
    test['data'] = list(test_docs.values())
    test['labels'] = labels_test

    return do_create(train, test)


def do_create(train, test):
    """
    print(train.head())
    print('Training sample:', train['data'][0])
    print('Author of sample:', train['labels'][0])
    print('Training Data Shape:', train.shape)
    print('Testing Data Shape:', test.shape)

    print('Training Dataset Info:')
    print(train.info())

    print('Testing Dataset Info:')
    print(test.info())
    """
    """
    # Barplot of occurances of each author in the training dataset
    sns.barplot(x=['Flüchtlinge', 'Merkel', 'Seehofer'],
                y=train['labels'].value_counts())
    plt.show()
    """

    # preprocessing
    print('removing stop words')
    nlp = spacy.load('de')
    stop_words = get_stop_words('de')
    stop_words.append('foto')
    stop_words.append('picture')

    for stopword in stop_words:
        lexeme = nlp.vocab[stopword]
        lexeme.is_stop = True

    """
    # Parse documents and print some info
    print('Parsing documents...')

    start = time.time()

    train_vec = []
    for doc in nlp.pipe(train_cleaned, batch_size=500):
        if doc.has_vector:
            train_vec.append(doc.vector)
        # If doc doesn't have a vector, then fill it with zeros.
        else:
            train_vec.append(np.zeros((128,), dtype="float32"))

    # train_vec = [doc.vector for doc in nlp.pipe(train_cleaned, batch_size=500)]
    train_vec = np.array(train_vec)

    end = time.time()
    print('Total time passed parsing documents: {} seconds'.format(end - start))
    print('Total number of documents parsed: {}'.format(len(train_vec)))
    print('Number of words in first document: ', len(train['data'][0]))
    print('Number of words in second document: ', len(train['data'][1]))
    print('Size of vector embeddings: ', train_vec.shape[1])
    print('Shape of vectors embeddings matrix: ', train_vec.shape)
    """

    # spacy
    # Clean text before feeding it to spaCy
    print('Original training data shape: ', train['data'].shape)
    train_cleaned = get_spacy_corpus(train['data'], nlp, logging=True)
    print('Cleaned up training data shape: ', train_cleaned.shape)

    # Word2Vec
    if test is not None:
        all_text = np.concatenate((train['data'], test['data']), axis=0)
    else:
        all_text = np.vstack(train['data'])
    all_text = pd.DataFrame(all_text, columns=['data'])
    print('Number of total text documents:', len(all_text))
    train_cleaned_word2vec = cleanup_text_word2vec(all_text['data'], nlp, logging=True)
    print('Cleaned up training data size (i.e. number of sentences): ', len(train_cleaned_word2vec))

    text_dim = 300
    print("Training Word2Vec model...")
    wordvec_model = Word2Vec(train_cleaned_word2vec, size=text_dim, window=5, min_count=3, workers=4, sg=1)
    print("Word2Vec model created.")
    print("%d unique words represented by %d dimensional vectors" % (len(wordvec_model.wv.vocab), text_dim))

    # Evaluation
    print(wordvec_model.wv.most_similar(positive=['frau', 'kanzlerin'], negative=['mann']))
    print('----')
    print(wordvec_model.wv.most_similar_cosmul(positive=['mann', 'kanzlerin'], negative=['frau']))
    print(wordvec_model.wv.doesnt_match("csu spd flüchtlinge merkel seehofer italien wahl".split()))
    print(wordvec_model.wv.similarity('afd', 'csu'))
    print(wordvec_model.wv.similarity('afd', 'spd'))
    print(wordvec_model.wv.similarity('afd', 'cdu'))
    print(wordvec_model.wv.similarity('afd', 'rechts'))
    print(wordvec_model.wv.similarity('afd', 'links'))

    # Create word vectors
    train_cleaned_vec = np.zeros((train.shape[0], text_dim), dtype="float32")  # 19579 x 300
    for i in range(len(train_cleaned)):
        train_cleaned_vec[i] = create_average_vec(train_cleaned[i], wordvec_model)

    print("Train word vector shape:", train_cleaned_vec.shape)

    y_train_ohe = label_binarize(train['labels'], classes=['JF', 'SPON', 'SZ'])
    print('y_train_ohe shape: {}'.format(y_train_ohe.shape))
    print('y_train_ohe samples:')
    print(y_train_ohe[:5])

    X_train, X_test, y_train, y_test = train_test_split(train_cleaned_vec, y_train_ohe, test_size=0.2)
    print('X_train size: {}'.format(X_train.shape))
    print('X_test size: {}'.format(X_test.shape))
    print('y_train size: {}'.format(y_train.shape))
    print('y_test size: {}'.format(y_test.shape))

    return X_train, X_test, y_train, y_test, wordvec_model



def do_create_twitter(train, test):
    # preprocessing
    print('removing stop words')
    nlp = spacy.load('de')
    stop_words = get_stop_words('de')
    stop_words.append('foto')
    stop_words.append('picture')

    for stopword in stop_words:
        lexeme = nlp.vocab[stopword]
        lexeme.is_stop = True


    # spacy
    # Clean text before feeding it to spaCy
    print('Original training data shape: ', train['data'].shape)
    train_cleaned = get_spacy_corpus(train['data'], nlp, logging=True)
    print('Cleaned up training data shape: ', train_cleaned.shape)

    # Word2Vec
    if test is not None:
        all_text = np.concatenate((train['data'], test['data']), axis=0)
    else:
        all_text = np.vstack(train['data'])
    all_text = pd.DataFrame(all_text, columns=['data'])
    print('Number of total text documents:', len(all_text))
    train_cleaned_word2vec = cleanup_text_word2vec(all_text['data'], nlp, logging=True)
    print('Cleaned up training data size (i.e. number of sentences): ', len(train_cleaned_word2vec))

    text_dim = 300
    print("Training Word2Vec model...")
    wordvec_model = Word2Vec(train_cleaned_word2vec, size=text_dim, window=5, min_count=3, workers=4, sg=1)
    print("Word2Vec model created.")
    print("%d unique words represented by %d dimensional vectors" % (len(wordvec_model.wv.vocab), text_dim))

    # Evaluation
    try:
        print(wordvec_model.wv.most_similar(positive=['frau', 'kanzlerin'], negative=['mann']))
        print('----')
        print(wordvec_model.wv.most_similar_cosmul(positive=['mann', 'kanzlerin'], negative=['frau']))
        print(wordvec_model.wv.doesnt_match("csu spd flüchtlinge merkel seehofer italien wahl".split()))
        print(wordvec_model.wv.similarity('afd', 'csu'))
        print(wordvec_model.wv.similarity('afd', 'spd'))
        print(wordvec_model.wv.similarity('afd', 'cdu'))
        print(wordvec_model.wv.similarity('afd', 'rechts'))
        print(wordvec_model.wv.similarity('afd', 'links'))
    except KeyError:
        pass

    # Create word vectors
    train_cleaned_vec = np.zeros((train.shape[0], text_dim), dtype="float32")  # 19579 x 300
    for i in range(len(train_cleaned)):
        train_cleaned_vec[i] = create_average_vec(train_cleaned[i], wordvec_model)

    print("Train word vector shape:", train_cleaned_vec.shape)

    #y_train_ohe = label_binarize(train['labels'], classes=['1', '0'])
    y = np.vstack(train['labels'])
    y_train_ohe  = np.array([[1,0] if i==1 else [0,1] for i in y])
    print('y_train_ohe shape: {}'.format(y_train_ohe.shape))
    print('y_train_ohe samples:')
    print(y_train_ohe[:5])

    X_train, X_test, y_train, y_test = train_test_split(train_cleaned_vec, y_train_ohe, test_size=0.2)
    print('X_train size: {}'.format(X_train.shape))
    print('X_test size: {}'.format(X_test.shape))
    print('y_train size: {}'.format(y_train.shape))
    print('y_test size: {}'.format(y_test.shape))
    return X_train, X_test, y_train, y_test, wordvec_model, train_cleaned_vec, y_train_ohe



def pack_data_to_predict(predict_file, wordvec_model_article, wordvec_model_tweet):
    df = utils.get_df(predict_file)
    # preprocessing
    print('removing stop words')
    nlp = spacy.load('de')
    stop_words = get_stop_words('de')
    stop_words.append('foto')
    stop_words.append('picture')

    for stopword in stop_words:
        lexeme = nlp.vocab[stopword]
        lexeme.is_stop = True

    # spacy
    # Clean text before feeding it to spaCy
    print('Original training data shape: ', df['article_text'].shape)
    predict_cleaned_article = get_spacy_corpus(df['article_text'], nlp, logging=True)
    print('Cleaned up training data shape: ', predict_cleaned_article.shape)

    text_dim = 300

    # Create word vectors
    predict_cleaned_vec = np.zeros((df.shape[0], text_dim), dtype="float32")
    for i in range(len(predict_cleaned_article)):
        predict_cleaned_vec[i] = create_average_vec(predict_cleaned_article[i], wordvec_model_article)


    predict_cleaned_tweet = get_spacy_corpus(df['tweet_text'], nlp, logging=True)
    print('Cleaned up training data shape: ', predict_cleaned_tweet.shape)

    text_dim = 300

    # Create word vectors
    predict_cleaned_vec_tweet = np.zeros((df.shape[0], text_dim), dtype="float32")
    for i in range(len(predict_cleaned_tweet)):
        predict_cleaned_vec_tweet[i] = create_average_vec(predict_cleaned_tweet[i], wordvec_model_tweet)
    #TODO: meta data
    return np.concatenate([predict_cleaned_vec, predict_cleaned_vec_tweet], axis=1)


    """
    # punctuations = string.punctuation
    # Grab all text associated with Edgar Allen Poe
    jf_text = [text for text in train[train['labels'] == 'JF']['data']]

    # Grab all text associated with H.P. Lovecraft
    spon_text = [text for text in train[train['labels'] == 'SPON']['data']]

    # Grab all text associated with Mary Wollstonecraft Shelley
    zeit_text = [text for text in train[train['labels'] == 'ZEIT']['data']]

    # Clean up all text
    jf_clean = get_spacy_corpus(jf_text, nlp)
    #jf_clean = ' '.join(jf_clean).split()

    spon_clean = get_spacy_corpus(spon_text, nlp)
    #spon_clean = ' '.join(spon_clean).split()

    zeit_clean = get_spacy_corpus(zeit_text, nlp)
    #zeit_clean = ' '.join(zeit_clean).split()

    # Count all unique words
    jf_counts = Counter(jf_clean)
    spon_counts = Counter(spon_clean)
    zeit_counts = Counter(zeit_clean)

    # Plot top 25 most frequently occuring words for Edgar Allen Poe
    jf_common_words = [word[0] for word in jf_counts.most_common(25)]
    jf_common_counts = [word[1] for word in jf_counts.most_common(25)]

    plt.figure(figsize=(15, 12))
    sns.barplot(x=jf_common_words, y=jf_common_counts)
    plt.title('Most Common Words used by JF')
    plt.show()

    print('Original training data shape: ', train['Text'].shape)
    """

    """
    VISUALIZATION
    # Combine all training text into one large string
    all_text = ' '.join([text for text in train['data']])
    print('Number of words in all_text:', len(all_text))

    # Word cloud for entire training dataset
    # default width=400, height=200
    wordcloud = WordCloud(width=800, height=500,
                          random_state=21, max_font_size=110).generate(all_text)
    plt.figure(figsize=(15, 12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

    # Grab all text that is written by JF
    jf = train[train['labels'] == 'JF']
    jf_text = ' '.join(text for text in jf['data'])
    print('Number of words in eap_text:', len(jf_text))
    wordcloud = WordCloud(width=800, height=500,
                          random_state=21, max_font_size=110).generate(jf_text)
    plt.figure(figsize=(15, 12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()
    """
    """
    http://localhost:8888/notebooks/text_analysis_tutorial.ipynb
    n_components = 3
    true_k = np.unique(labels).shape[0]
    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=get_stop_words('de'), use_idf=True)
    X_train = vectorizer.fit_transform(train['data'])
    svd = TruncatedSVD(n_components)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)
    X_train = lsa.fit_transform(X_train)

    y_train, y_test = train['labels'], test['labels']
    print("Extracting features from the test data using the same vectorizer")
    X_test = vectorizer.transform(test['data'])
    X_test = lsa.fit_transform(X_test)

    gnb = GaussianNB()
    y_pred_NB = gnb.fit(X_train, y_train).predict(X_test)

    svm = SVC()
    y_pred_SVM = svm.fit(X_train, y_train).predict(X_test)
    """




def create_word_vecs(articles, articles_test):
    if os.path.isfile('data/obj/X_train.pkl'):
        X_train = load_obj('X_train')
        X_test = load_obj('X_test')
        y_train = load_obj('y_train')
        y_test = load_obj('y_test')
    else:
        X_train, X_test, y_train, y_test, word2vec_model = prepare_scraped_data(articles, articles_test)
        save_obj(X_train, 'X_train')
        save_obj(X_test, 'X_test')
        save_obj(y_train, 'y_train')
        save_obj(y_test, 'y_test')
        save_obj(word2vec_model, 'word2vec_model')
    if os.path.isfile('data/obj/word2vec_model.pkl'):
        word2vec_model = load_obj('word2vec_model')
    else:
        X_train, X_test, y_train, y_test, word2vec_model = prepare_scraped_data(articles, articles_test)
        save_obj(X_train, 'X_train')
        save_obj(X_test, 'X_test')
        save_obj(y_train, 'y_train')
        save_obj(y_test, 'y_test')
        save_obj(word2vec_model, 'word2vec_model')
    return X_train, X_test, y_train, y_test, word2vec_model

def create_word_vecs_from_twitter(data_file, type_of_analysis):
    if os.path.isfile('data/obj/twitter/' + type_of_analysis + '/X_train.pkl') and \
            os.path.isfile('data/obj/twitter/' + type_of_analysis + '/word2vec_model.pkl') and \
            os.path.isfile('data/obj/twitter/' + type_of_analysis + '/train_cleaned_vec.pkl'):
        X_train = load_obj('twitter/' + type_of_analysis + '/X_train')
        X_test = load_obj('twitter/' + type_of_analysis + '/X_test')
        y_train = load_obj('twitter/' + type_of_analysis + '/y_train')
        y_test = load_obj('twitter/' + type_of_analysis + '/y_test')
        word2vec_model = load_obj('twitter/' + type_of_analysis + '/word2vec_model')
        train_cleaned_vec = load_obj('twitter/' + type_of_analysis + '/train_cleaned_vec')
        y_train_ohe = load_obj('twitter/' + type_of_analysis + '/y_train_ohe')
    else:
        X_train, X_test, y_train, y_test, word2vec_model, train_cleaned_vec, y_train_ohe = prepare_twitter_data(data_file, type_of_analysis)
        save_obj(X_train, 'twitter/' + type_of_analysis + '/X_train')
        save_obj(X_test, 'twitter/' + type_of_analysis + '/X_test')
        save_obj(y_train, 'twitter/' + type_of_analysis + '/y_train')
        save_obj(y_test, 'twitter/' + type_of_analysis + '/y_test')
        save_obj(word2vec_model, 'twitter/' + type_of_analysis + '/word2vec_model')
        save_obj(train_cleaned_vec, 'twitter/' + type_of_analysis + '/train_cleaned_vec')
        save_obj(y_train_ohe, 'twitter/' + type_of_analysis + '/y_train_ohe')
    return X_train, X_test, y_train, y_test, word2vec_model, train_cleaned_vec, y_train_ohe



