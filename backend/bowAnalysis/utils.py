import pickle


def save_obj(obj, path, name, test_string = ''):
    with open(path + name + test_string + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path, name, test_string=''):
    with open(path + name + test_string + '.pkl', 'rb') as f:
        return pickle.load(f)