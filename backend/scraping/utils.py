


def update_progress(data):
    import pickle
    from .. import constants
    with open(constants.PROGRESSFILE_SCRAPER, 'wb') as fp:
        pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)