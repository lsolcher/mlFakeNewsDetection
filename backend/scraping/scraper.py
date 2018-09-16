from . import SponScraper, SzScraper, JungeFreiheitScraper, utils
import traceback, os
from .. import constants
from pathlib import Path

def scrape():
    try:
        prepare_progress_file()
        progress = ['Starter Artikelanalyse']
        utils.update_progress(progress)
        print('-------')
        print('Scraping SZ')
        print('-------')
        progress = SzScraper.scrape(progress)
        print('-------')
        print('Scraping JF')
        print('-------')
        progress = JungeFreiheitScraper.scrape(progress)
        print('-------')
        print('Scraping SPON')
        print('-------')
        progress = SponScraper.scrape(progress)
        return True
    except:
        traceback.print_exc()
        return False


def prepare_progress_file():
    if not os.path.exists(constants.ARTICLE_FOLDER):
        os.makedirs(constants.ARTICLE_FOLDER)
    Path(constants.PROGRESSFILE_SCRAPER).touch(exist_ok=True)
    with open(constants.PROGRESSFILE_SCRAPER, "w"):
        pass