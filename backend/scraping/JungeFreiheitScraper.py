# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:09:57 2018

@author: Luc
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
import traceback
from backend import constants
from pathlib import Path
from .utils import update_progress

RESULTPATH = constants.ARTICLE_FOLDER

def scrape(progress):
    # Websites to scrape
    URL = []
    URL.append('https://jungefreiheit.de/kategorie/politik/')
    URL.append('https://jungefreiheit.de/kategorie/wirtschaft/')
    URL.append('https://jungefreiheit.de/kategorie/kultur/')
    URL.append('https://jungefreiheit.de/kategorie/wissen/')
    URL.append('https://jungefreiheit.de/kategorie/debatte/')
    PAGE = []
    for url in URL:
        PAGE.append(urlopen(url))
    soup_mainpages = []
    for page in PAGE:
        soup_mainpages.append(BeautifulSoup(page, 'html.parser'))

    progress.append('Analysiere aktuelle Artikel von www.jungefreiheit.de')
    progress.append('Sammle Artikel...')
    # progress.progress_value = 0
    update_progress(progress)

    # get all article URLs
    article_links = set()
    for i, category in enumerate(soup_mainpages):
        for iteration in range(0, 100):
            try:
                if iteration > 0:
                    nextUrlTag = category.find('a', href=True, text=re.compile('Nächste Seite'))
                    URL[i] = nextUrlTag['href']
                    PAGE[i] = urlopen(URL[i])
                    category = BeautifulSoup(PAGE[i], 'html.parser')
                for link in category.findAll('a', attrs={'href': re.compile("^https://jungefreiheit.de/.*")}):
                    if link['href'] and '2018' in link['href'] and '/#comments' not in link['href']:  # eliminate non-articles
                        article_links.add(link['href'])
                        if len(article_links) % 100 == 0:
                            print('Fetching articles. Found {} unique articles so far.'.format(len(article_links)))
                            prog_str = ('Bisher wurden {} Artikel von Junge Freiheit gefunden'.format(len(article_links)))
                            if prog_str not in progress:
                                # because some article urls are found more than once and
                                # won't be added twice but counting still thinks somethin new is added
                                progress.append(prog_str)
                                update_progress(progress)
            except TypeError:
                traceback.print_exc()
                iteration = 100
                i += 1
            except Exception:
                traceback.print_exc()

    progress.append('Neue Artikel gesammelt!')
    progress.append('Insgesamt wurden {} Artikel gefunden.'.format(len(article_links)))
    progress.append('Gleiche mit Datenbank ab...')
    # progress.progress_value = 11
    update_progress(progress)
    result_url_file = RESULTPATH + '\\jf_urls.txt'
    Path(result_url_file).touch(exist_ok=True)
    old_links = set(line.strip() for line in open(result_url_file))
    article_links = set(article_links)  # eliminate duplicate entries
    new_links = article_links - old_links # get only new - not already saved urls
    print('Found {} new items since last scan'.format(len(new_links)))
    with open(result_url_file, 'a') as f:
        for item in new_links:
            f.write("%s\n" % item.rstrip('/'))
    progress.append('{} neue Artikel seit dem letzten Scan gefunden. \n Schreibe Artikel in Datenbank...'.format(len(new_links)))
    update_progress(progress)

    print('Found {} unique articles in total. Start writing...'.format(len(new_links)))
    # get article text and save it to file
    print(len(new_links))
    for idx, url in enumerate(new_links):
        try:
            if idx % 100 == 0:
                print('Wrote {} of {} articles.'.format(idx, len(new_links)))
                progress.append('Schreibe Artikel...')
                progress.append('Bisher wurden {} von {} Artikel geschrieben.'.format\
                    (idx, len(new_links)))
                update_progress(progress)
            page = urlopen(url)
            soup_article = BeautifulSoup(page, 'html.parser')
            article = soup_article.find("div", {"class": "entry-content"}).findAll('p')
            text = ''
            for idy, element in enumerate(article):
                if idy < len(article) - 1 and idy != 0: # remove press agency parentheses and header
                    text += ''.join(element.findAll(text=True))
            text = re.sub(r"\b[A-Z]+(?:\s+[A-Z]+)*\b. ", '', text)  # remove uppercased city
            if text:
                fields = [url.rstrip('/'),
                          text]
                result_article_file = RESULTPATH + '\\jf.csv'
                Path(result_article_file).touch(exist_ok=True)
                with open(result_article_file, 'a+', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter='|')
                    writer.writerow(fields)
        except Exception:
            print(Exception)
            traceback.print_exc()

    progress.append('Datenbank mit neuesten Artikeln von www.jungefreiheit.de erfolgreich aktualisiert!')
    progress.append('Insgesamt wurden {} neue Artikel in die Datenbank geschrieben.'.format(len(new_links)))
    # progress.progress_value = 33
    update_progress(progress)
    return progress

