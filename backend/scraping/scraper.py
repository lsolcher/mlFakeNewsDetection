from . import SponScraper, SzScraper, JungeFreiheitScraper
import traceback


def scrape():
    try:
        print('-------')
        print('Scraping SZ')
        print('-------')
        SzScraper.scrape()
        print('-------')
        print('Scraping JF')
        print('-------')
        JungeFreiheitScraper.scrape()
        print('-------')
        print('Scraping SPON')
        print('-------')
        SponScraper.scrape()
        return True
    except:
        traceback.print_exc()
        return False
