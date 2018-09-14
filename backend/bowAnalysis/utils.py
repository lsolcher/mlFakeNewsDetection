import pickle
from .. import constants


def save_obj(obj, path, name, test_string = ''):
    with open(path + name + test_string + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path, name, test_string=''):
    with open(path + name + test_string + '.pkl', 'rb') as f:
        return pickle.load(f)

def update_progress(data):
    with open(constants.PROGRESSFILE_BOW, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)

def get_progress():
    with open(constants.PROGRESSFILE_BOW, 'rb') as fp:
        progress = pickle.load(fp)
    return progress