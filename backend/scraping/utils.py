


def update_progress(data):
    import pickle
    from .. import constants
    with open(constants.PROGRESSFILE, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)