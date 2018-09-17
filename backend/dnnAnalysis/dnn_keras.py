from .create_word_vector import create_word_vecs, create_word_vecs_from_twitter, pack_data_to_predict
from .prepare_meta_data import create_train_test_from_twitter, create_meta_data_from_twitter
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Input, LSTM, Bidirectional, Flatten
from keras.layers import Conv1D, MaxPooling1D, GlobalMaxPooling1D
from keras.optimizers import SGD
from keras import backend
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.metrics import log_loss
import os
from sklearn.model_selection import train_test_split
import pandas as pd
from . import utils
from backend import constants
from collections import Counter

CURRENTFOLDER = constants.CURRENTFOLDER
DATAFOLDER = constants.DATAFOLDER
TWITTER_DATA_FILE = constants.TWITTER_DATA_FILE
TEST_DATA_FILE = constants.TEST_DATA_FILE
MODEL_FOLDER = constants.MODEL_FOLDER


OUTPUT_LABELS = 2
CLASS_WEIGHT = {0: 30.,
                1: 1.}
X_SHAPE = 408

def build_model(architecture='mlp'):
    model = Sequential()
    if architecture == 'mlp':
        #model.add(BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
        #                                beta_initializer='zeros', gamma_initializer='ones',
        #                                moving_mean_initializer='zeros', moving_variance_initializer='ones',
        #                                 beta_regularizer=None, gamma_regularizer=None, beta_constraint=None,
        #                                 gamma_constraint=None))
        #model.add(Dense(512, input_dim=X_SHAPE,
        #                kernel_regularizer=regularizers.l2(0.01),
        #                activity_regularizer=regularizers.l1(0.01)))
        # Densely Connected Neural Network (Multi-Layer Perceptron)
        model.add(Dense(512, activation='relu', kernel_initializer='he_normal', input_dim=X_SHAPE))
        model.add(Dropout(0.2))
        model.add(Dense(512, activation='relu', kernel_initializer='he_normal'))
        model.add(Dropout(0.2))
        model.add(Dense(256, activation='relu', kernel_initializer='he_normal'))
        model.add(Dropout(0.2))
        model.add(Dense(128, activation='relu', kernel_initializer='he_normal'))
        model.add(Dropout(0.2))
        model.add(Dense(OUTPUT_LABELS, activation='softmax'))
    elif architecture == 'cnn':
        # 1-D Convolutional Neural Network
        inputs = Input(shape=(X_SHAPE,1))

        x = Conv1D(64, 3, strides=1, padding='same', activation='relu')(inputs)

        #Cuts the size of the output in half, maxing over every 2 inputs
        x = MaxPooling1D(pool_size=2)(x)
        x = Conv1D(128, 3, strides=1, padding='same', activation='relu')(x)
        x = GlobalMaxPooling1D()(x)
        outputs = Dense(OUTPUT_LABELS, activation='softmax')(x)

        model = Model(inputs=inputs, outputs=outputs, name='CNN')
    elif architecture == 'lstm':
        # LSTM network
        inputs = Input(shape=(X_SHAPE,1))

        x = Bidirectional(LSTM(64, return_sequences=True),
                          merge_mode='concat')(inputs)
        x = Dropout(0.2)(x)
        x = Flatten()(x)
        outputs = Dense(3, activation='softmax')(x)

        model = Model(inputs=inputs, outputs=outputs, name='LSTM')
    else:
        print('Error: Model type not found.')
    return model

def analyze_tweet(tweet):
    w2v_article = utils.load_obj(constants.ARTICLE_TEXT_MODEL_FOLDER, 'word2vec_model')
    w2v_tweet = utils.load_obj(constants.TWEET_TEXT_MODEL_FOLDER, 'word2vec_model')
    MODELNAME = 'sequential_1_twitter'
    if os.path.exists(os.path.join(MODEL_FOLDER, MODELNAME)):
        model = load_model(os.path.join(MODEL_FOLDER, MODELNAME))
        return predict(model, tweet, w2v_article, w2v_tweet)

def analyze_article(url, article_string):
    w2v_article = utils.load_obj(constants.ARTICLE_TEXT_MODEL_FOLDER, 'word2vec_model')
    MODELNAME = 'sequential_1_article'
    article = {'article_url': url,
               'article_text': article_string}
    if os.path.exists(os.path.join(MODEL_FOLDER, MODELNAME)):
        model = load_model(os.path.join(MODEL_FOLDER, MODELNAME))
        return predict(model, article, w2v_article)


def run(articles, articles_test, twitter_data, text_analysis=True, all_features=True, train_model=True):
    if train_model:
        TYPE_OF_ANALYSIS = 'article_text'  # by content of article
        #TYPE_OF_ANALYSIS = 'tweet_text'  # by content of tweet
        df = pd.read_csv(TWITTER_DATA_FILE, sep='|', encoding='utf-8', keep_default_na=False)
        print('removing duplicates')
        df = utils.remove_duplicates(df)
        idx1 = idx2 = None
        if twitter_data:
            if all_features:
                X_train_article, X_test_article, y_train_article, y_test_article, w2v_article, train_cleaned_vec_article, y_train_ohe_article = create_word_vecs_from_twitter(
                    TWITTER_DATA_FILE, type_of_analysis='article_text')
                X_train_tweet, X_test_tweet, y_train_tweet, y_test_tweet, w2v_tweet, train_cleaned_vec_tweet, y_train_ohe_tweet = create_word_vecs_from_twitter(
                    TWITTER_DATA_FILE, type_of_analysis='tweet_text')
                X_meta = create_meta_data_from_twitter(TWITTER_DATA_FILE)
                train_cleaned_vec = np.concatenate([train_cleaned_vec_article, train_cleaned_vec_tweet, X_meta], axis=1)#
                y_train_ohe = y_train_ohe_article

                scaler = StandardScaler()
                scaler.fit(train_cleaned_vec)
                scaled_features = scaler.transform(train_cleaned_vec)
                print(scaled_features)

                X_train, X_test, y_train, y_test, idx1, idx2 = train_test_split(scaled_features, y_train_ohe, df['tweet_url'], test_size=0.4)
            else:
                if text_analysis:
                    X_train, X_test, y_train, y_test, w2v, train_cleaned_vec, y_train_ohe = create_word_vecs_from_twitter(TWITTER_DATA_FILE, type_of_analysis=TYPE_OF_ANALYSIS)
                else:
                    X_train, X_test, y_train, y_test = create_train_test_from_twitter(TWITTER_DATA_FILE)
        else:
            X_train, X_test, y_train, y_test, w2v = create_word_vecs(articles, articles_test)

        train(X_train, X_test, y_train, y_test, id_train=idx1, id_test=idx2)
        # TODO:

        MODELNAME = 'sequential_1'

        if os.path.exists(os.path.join(MODEL_FOLDER, MODELNAME)):

            model = load_model(os.path.join(MODEL_FOLDER, MODELNAME))
            predict(model, TEST_DATA_FILE, w2v_article, w2v_tweet)
    else:
        print('not yet implemented')


def predict(model, predict_file, w2v_article, w2v_tweet=None):
    print('predicting')
    if w2v_tweet: # predict a tweet with scaler for article_text, tweet_text, metadata
        X_test = pack_data_to_predict(predict_file, w2v_article, w2v_tweet)
        print(X_test)
        X_meta = create_meta_data_from_twitter(predict_file)
        x_predict = np.concatenate([X_test, X_meta], axis=1)
        scaler = utils.load_obj(constants.OBJECT_FOLDER, 'scaler')
    else:  # predicting an article
        x_predict = pack_data_to_predict(predict_file, w2v_article)
        scaler = utils.load_obj(constants.OBJECT_FOLDER, 'scaler_article')
    print(x_predict)
    scaled_features = scaler.transform(x_predict)
    if model.name == "CNN" or model.name == "LSTM":
        scaled_features = np.expand_dims(scaled_features, axis=2)

    predicted_prob = model.predict(scaled_features)
    print(scaled_features.shape)
    df = utils.get_df(predict_file)
    if w2v_tweet:
        predict_urls = df['tweet_url'].tolist()
    else:
        predict_urls = df['article_url'].tolist()


    # Save submission file
    with open(DATAFOLDER + '/predict.csv', 'w', encoding='utf-8') as file_obj:
        file_obj.write('ID|FAKE|NOT_FAKE\n')
        for pred in range(len(predicted_prob)):
            file_obj.write(
                str(predict_urls[pred]) + '|' + '|'.join('{:.2f}'.format(s) for s in predicted_prob[pred].tolist()) + '\n')
    print('saved result file to {}'.format('predict.csv'))
    # clean up after prediction
    del model
    backend.clear_session()
    return predicted_prob



def get_class_weights(y_ohe):
    y = [np.where(r == 1)[0][0] for r in y_ohe]
    counter = Counter(y)
    majority = max(counter.values())
    return  {cls: float(majority/count) for cls, count in counter.items()}



def train(X_train, X_test, y_train, y_test, id_train=None, id_test=None):
    print('X_train size: {}'.format(X_train.shape))
    print('X_test size: {}'.format(X_test.shape))
    print('y_train size: {}'.format(y_train.shape))
    print('y_test size: {}'.format(y_test.shape))



    model = build_model('mlp')


    if model.name == "CNN" or model.name == "LSTM":
        X_train = np.expand_dims(X_train, axis=2)
        X_test = np.expand_dims(X_test, axis=2)
        print('Text train shape: ', X_train.shape)
        print('Text test shape: ', X_test.shape)

    model.summary()

    # Compile the model
    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['acc'])

    # Define number of epochs
    epochs = 15

    print(get_class_weights(y_train))
    # Fit the model to the training data
    estimator = model.fit(X_train, y_train,
                          validation_split=0.4,
                          epochs=epochs, batch_size=128, verbose=1, class_weight=get_class_weights(y_train))

    print("Training accuracy: %.2f%% / Validation accuracy: %.2f%%" %
          (100 * estimator.history['acc'][-1], 100 * estimator.history['val_acc'][-1]))
    # Plot model accuracy over epochs
    sns.reset_orig()
    plt.plot(estimator.history['acc'])
    plt.plot(estimator.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'valid'], loc='upper left')
    plt.savefig('accurary.png')
    plt.show()


    # Plot model loss over epochs
    plt.plot(estimator.history['loss'])
    plt.plot(estimator.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'valid'], loc='upper left')
    plt.savefig('loss.png')
    plt.show()


    model.save(model.name)

    # Make predictions
    predicted_prob = model.predict(X_test)
    print(predicted_prob.shape)
    if id_test is not None:
        id_test = id_test.values
    # Save submission file
    with open('submission.csv', 'w') as file_obj:
        file_obj.write('ID|FAKE|NOT_FAKE\n')
        for pred in range(len(predicted_prob)):
            if id_test is None:
                file_obj.write(
                    str(y_test[pred]) + '|' + '|'.join(
                        '{:.2f}'.format(s) for s in predicted_prob[pred].tolist()) + '\n')
            else:
                file_obj.write(
                    str(id_test[pred]) + '|' + str(y_test[pred]) + '|' + '|'.join(
                        '{:.2f}'.format(s) for s in predicted_prob[pred].tolist()) + '\n')
    # Report log loss and score
    loss_sk = log_loss(y_test, predicted_prob)
    print('Log loss is: {}'.format(loss_sk))
