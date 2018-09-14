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
from .utils import update_progress
from pathlib import Path

RESULTPATH = constants.ARTICLE_FOLDER

def scrape(progress):
    # Websites to scrape
    URL = []
    URL.append('http://www.spiegel.de/politik/')
    URL.append('http://www.spiegel.de/thema/meinung/')
    URL.append('http://www.spiegel.de/wirtschaft/')
    URL.append('http://www.spiegel.de/panorama/')
    URL.append('http://www.spiegel.de/kultur/')
    PAGE = []
    for url in URL:
        PAGE.append(urlopen(url))
    soup_mainpages = []
    for page in PAGE:
        soup_mainpages.append(BeautifulSoup(page, 'html.parser'))

    progress.append('Analysiere aktuelle Artikel von www.sueddeutsche.de')
    progress.append('Sammle Artikel...')
    # progress.progress_value = 0
    update_progress(progress)

    # get all article URLs
    article_links = set()
    for i, category in enumerate(soup_mainpages):
        for iteration in range(0, 10):
            try:
                if iteration > 0:
                    nextUrlTag = category.find('a', href=True, text='Mehr Artikel')
                    URL[i] = 'http://www.spiegel.de'+ nextUrlTag['href']
                    PAGE[i] = urlopen(URL[i])
                    category = BeautifulSoup(PAGE[i], 'html.parser')
                for link in category.findAll('a', attrs={'href': re.compile("^(?!http://.*$).*")}):
                    if '.html' in link['href'] and '-a-' in link['href'] and '/plus/' not in link['href'] \
                            and 'news-' not in link['href']: #eliminate non-articles - SPON marks artikels with -a-
                        article_links.add('http://www.spiegel.de' + link['href'])
                        if len(article_links) % 100 == 0:
                            print('Fetching articles. Found {} unique articles so far.'.format(len(article_links)))
                            progress.append('Bisher wurden {} Artikel gefunden'.format(len(article_links)))
                            update_progress(progress)

            except TypeError:
                traceback.print_exc()
                i += 1
            except Exception:
                traceback.print_exc()

    progress.append('Neue Artikel gesammelt!')
    progress.append('Insgesamt wurden {} Artikel gefunden.'.format(len(article_links)))
    progress.append('Gleiche mit Datenbank ab...')
    # progress.progress_value = 11
    update_progress(progress)

    result_url_file = RESULTPATH + '\\spon_urls.txt'
    Path(result_url_file).touch(exist_ok=True)
    old_links = set(line.strip() for line in open(result_url_file))
    article_links = set(article_links)  # eliminate duplicate entries
    new_links = article_links - old_links # get only new - not already saved urls
    print('Found {} new items since last scan'.format(len(new_links)))
    with open(result_url_file, 'a') as f:
        for item in new_links:
            f.write("%s\n" % item)

    progress.append('{} neue Artikel seit dem letzten Scan gefunden. \n Schreibe Artikel in Datenbank...'.format(len(new_links)))
    update_progress(progress)
    print('Found {} unique articles in total. Start writing...'.format(len(new_links)))

    # get article text and save it to file
    print(len(new_links))
    for idx, url in enumerate(new_links):
        try:
            page = urlopen(url)
            soup_article = BeautifulSoup(page, 'html.parser')
            all_text = ''
            for text in soup_article.findAll('p'):
                all_text += text.getText()
            all_text = all_text.split('Wer steckt hinter Civey?', 1)[0]
            all_text = all_text.split('© SPIEGEL ONLINE', 1)[0]
            all_text = all_text.replace('SPIEGEL ONLINE', '')
            all_text = all_text.replace('SPIEGEL+', '')
            all_text = all_text.replace('SPIEGEL', '')
            if all_text:
                fields = [url,
                          all_text]
                result_article_file = RESULTPATH + '\\spon.csv'
                Path(result_article_file).touch(exist_ok=True)
                with open(result_article_file, 'a+', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f, delimiter='|')
                    writer.writerow(fields)
            if idx % 100 == 0:
                print('Scraped {} of {} articles'.format(idx, len(new_links)))
                progress.append('Schreibe Artikel... \n Bisher wurden {} von {} Artikel geschrieben.'.format\
                    (idx, len(new_links)))
                update_progress(progress)
        except Exception:
            traceback.print_exc()


    progress.append('Datenbank mit neuesten Artikeln von www.spiegel.de erfolgreich aktualisiert!')
    progress.append('Insgesamt wurden {} neue Artikel in die Datenbank geschrieben.'.format(len(new_links)))
    # progress.progress_value = 33
    update_progress(progress)
    return progress
    
    

