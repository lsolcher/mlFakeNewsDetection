from . import SponScraper, SzScraper, JungeFreiheitScraper


def scrape():
    try:
        SzScraper.scrape()
        JungeFreiheitScraper.scrape()
        SponScraper.scrape()
        return True
    except:
        return False
