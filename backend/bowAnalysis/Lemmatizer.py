from germalemma import GermaLemma


def lemmatize_tokens(tokens):
    lemmatizer = GermaLemma()
    new_tokens = {}
    for doc_label, tok_pos in tokens.items():
        lemmata_pos = []
        for t, pos in tok_pos:
            try:
                l = lemmatizer.find_lemma(t, pos)
            except ValueError:
                l = t
            lemmata_pos.append((l, pos))
            new_tokens[doc_label] = lemmata_pos

    return new_tokens

