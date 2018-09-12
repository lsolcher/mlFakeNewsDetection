# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:09:57 2018

@author: Luc
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import logging
import os.path
import csv
from backend import constants
from pathlib import Path

RESULTPATH = constants.ARTICLE_FOLDER

def scrape():
    if not os.path.exists(RESULTPATH):
        os.makedirs(RESULTPATH)
    logger = logging.getLogger('root')
    logger.info('start scraping spon')

    # Websites to scrape
    URL = []
    URL.append('https://www.sueddeutsche.de/archiv/politik/2018/page/')
    URL.append('https://www.sueddeutsche.de/archiv/panorama/2018/page/')
    URL.append('https://www.sueddeutsche.de/archiv/wirtschaft/2018/page/')
    URL.append('https://www.sueddeutsche.de/archiv/kultur/2018/page/')
    PAGE = []
    for url in URL:
        PAGE.append(None)

    max_pages = 10

    # get all article URLs
    article_links = set()
    for i, category in enumerate(URL):
        for iteration in range(0, max_pages):
            try:
                this_url = URL[i] + str(iteration+1)
                PAGE[i] = urlopen(this_url)
                category = BeautifulSoup(PAGE[i], 'html.parser')
                for link in category.findAll('a', attrs={'href': re.compile("^(?!http://.*$).*")}):
                    if 'sueddeutsche' in link['href'] and \
                            'lesermarkt' not in link['href'] and \
                            'szshop' not in link['href'] and \
                            'https' in link['href'] and \
                            'www' in link['href'] and \
                            '-' in link['href'] and \
                            '1.4' not in link['href'] and \
                            'datenschutz' not in link['href'] and \
                            'wettervorhersage' not in link['href']:  # eliminate non-articles
                        article_links.add(link['href'])
                        if len(article_links) % 100 == 0:
                            print('Fetching articles. Found {} unique articles so far.'.format(len(article_links)))
                if iteration == max_pages - 1:
                    print('Done with category {}. Moving to the next one.'.format(i))
            except TypeError:
                logger.exception('Done with category {}. Moving to the next one.'.format(i))
                i += 1

            except Exception:
                logger.exception("Error while fetching links")

    result_url_file = RESULTPATH + '\\sz_urls.txt'
    Path(result_url_file).touch(exist_ok=True)
    old_links = set(line.strip() for line in open(result_url_file))
    article_links = set(article_links)  # eliminate duplicate entries
    new_links = article_links - old_links # get only new - not already saved urls
    print('Found {} new items since last scan'.format(len(new_links)))
    with open(result_url_file, 'a') as f:
        for item in new_links:
            f.write("%s\n" % item)

    # get article text and save it to file
    print(len(new_links))
    for idx, url in enumerate(new_links):
        try:
            page = urlopen(url)
            soup_article = BeautifulSoup(page, 'html.parser')
            all_text = ''
            p = soup_article.find('section', attrs={'class' : 'body'}).findAll('p')
            for text in p:
                all_text += ''.join(text.findAll(text=True))
            all_text = re.sub(r'.*\(*\) - ', '', all_text) # remove city and agency tags
            if all_text:
                if all_text:
                    fields = [url,
                              all_text]
                    result_article_file = RESULTPATH + '\\sz.csv'
                    Path(result_article_file).touch(exist_ok=True)
                    with open(result_article_file, 'a+', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f, delimiter='|')
                        writer.writerow(fields)
            if idx % 100 == 0:
                print('Scraped {} of {} articles'.format(idx, len(new_links)))
        except Exception:
            print(Exception)
            logger.exception("Error while parsing")




