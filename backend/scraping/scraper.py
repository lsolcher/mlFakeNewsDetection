from . import SponScraper, SzScraper, JungeFreiheitScraper


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
        return False
