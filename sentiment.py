def _load(name):
    fid = open(name + ".txt", encoding="latin-1")
    words = set()

    for line in fid:
        if line.startswith(";"):
            continue
        line = line.rstrip()
        if len(line) == 0:
            continue
        words.add(line)

    fid.close()

    return words


_pos_words = _load("positive-words")
_neg_words = _load("negative-words")

def get_sentiment(words):
    pos, neg = 0, 0
    for word in words:
        w = word.lower()
        if w in _pos_words:
            pos += 1
        if w in _neg_words:
            neg += 1
    return pos, neg
