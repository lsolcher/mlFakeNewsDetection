def process_article(url_input):
    try:
        r = requests.get(url_input)
        url = r.url  # twitter is redircecting - get the correct link
        if url is not None:
            all_text, all_hidden_text, article = is_article(url, check_for_duplicates=False)
            #  format text to not mess up csv writing
            all_text = all_text.replace('|', ';')  # we use | as csv delimiter so replace them
            all_text = all_text.replace('\n', ' ')
            all_text = all_text.replace('\r', ' ')
            all_text = all_text.rstrip()
            print('{}: Found Tweet with links'.format(datetime.datetime.now().time()))
            if article:
                return True, all_text
            else:
                return False, '{} verlinkt auf keinen Artikel'.format(url)
        else:
            return False, 'Konnte keine Artikel in {} finden.'.format(url)
    except:
        return False, 'Die Eingabe scheint weder eine Twitter-Id noch eine URL zu sein.'
