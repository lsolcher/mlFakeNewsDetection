from . import SponScraper, SzScraper, JungeFreiheitScraper
import traceback
from .. import constants
from pathlib import Path

def scrape():
    try:
        progress = []
        prepare_progress_file()
        print('-------')
        print('Scraping SZ')
        print('-------')
        progress = SzScraper.scrape(progress)
        print('-------')
        print('Scraping JF')
        print('-------')
        JungeFreiheitScraper.scrape(progress)
        print('-------')
        print('Scraping SPON')
        print('-------')
        SponScraper.scrape(progress)
        return True
    except:
        traceback.print_exc()
        return False


def prepare_progress_file():
    Path(constants.PROGRESSFILE).touch(exist_ok=True)
    with open(constants.PROGRESSFILE, "w"):
        pass