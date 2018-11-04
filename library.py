# for download()
import requests
# import os
# for clean_html()
from bs4 import BeautifulSoup
from bs4.element import Comment
import unicodedata
# for find_stats()
import nltk
nltk.download("punkt")
from math import ceil
from sentiment import get_sentiment
# for h2t()
# import html2text
# for np2t()
import newspaper
import time
import pickle

def get_html(url):
    # files = os.listdir("raw_html")
    req = requests.get(url.rstrip())
    html = req.text

    if html.lower() == "not found":
        return "ERROR"
    else:
        return html


def clean_html(html):
    def tag_visible(element):
        # print("HERE\n")
        # print(element.parent.name)
        # print(element)
        # print("\n")
        if element.parent.name in ["style", "script", "head", "title", "meta",
                                   "[document]", "span", "img", "svg", "li",
                                   "a"]:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(body):
        soup = BeautifulSoup(body, "html.parser")
        texts = soup.findAll(text=True)
        visible_texts = []
        """
        for element in texts:
            if tag_visible(element) == True:
                visible_texts.append(element)
        """
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def call_decompose(x):
        for _ in x.find_all("script"):
            x.script.decompose()
        for _ in x.find_all("li"):
            x.li.decompose()
        # for _ in x.find_all("span"):
            # x.span.decompose()
        for _ in x.find_all("img"):
            # print(_)
            x.img.decompose()
        for _ in x.find_all("table"):
            x.table.decompose()

        # print(x.get_text(), "\n")

    soup = BeautifulSoup(html, "html.parser")
    pars = []

    for x in soup.find_all("p"):
        # print("P-TAG:")
        call_decompose(x)
        pars.append(x.get_text())
    for i, x in enumerate(pars):
        pars[i] = unicodedata.normalize("NFKD", x)
        pars[i] = pars[i].replace("\t", " ")
        pars[i] = pars[i].replace("\r", "")
        pars[i] = pars[i].replace("\n\n", "\n")

    text = ". ".join(pars)
    text = text.replace(";", ".")

    if text == "":
        text = text_from_html(html)

    return text


# def h2t(html):
#    # text = html2text.html2text(html)
#    h = html2text.HTML2Text()
#    h.ignore_links = True
#    h.ignore_images = True
#    h.ignore_anchors = True
#    h.ignore_tables = True
#    text = h.handle(html)
#    text = re.sub("\[[^\]]*\]\([^\)]*\)", "", text)
#    return text

def np2t(url):

    if not url.startswith("http"):
        url = "http://" + url
    
    req = requests.get(url)
    html = req.text
    
    art = newspaper.Article(url)
    art.download(input_html=html)
    time.sleep(1)

    art.parse()
    text = art.text
    return text


def find_stats(text):

    sent_tokenizer = pickle.load(open("static/english.pickle", "rb"))
    
    statistics = {}
    sents = sent_tokenizer.tokenize(text)
    words = []
    for x in sents:
        words.extend(nltk.word_tokenize(x))

    total_words = len(words)
    statistics["total_words"] = total_words

    letters = "".join(words)
    total_letters = len(letters)
    statistics["total_letters"] = total_letters

    total_sents = len(sents)
    statistics["total_sents"] = total_sents

    if total_words > 0:
        statistics["avg_word_len"] = total_letters/total_words
    else:
        statistics["avg_word_len"] = 0

    if total_sents > 0:
        statistics["avg_sent_len"] = total_words/total_sents
    else:
        statistics["avg_sent_len"] = 0

    try:
        ari = (4.71*(total_letters/total_words) + 0.5*(total_words/total_sents) - 21.43)
    except ZeroDivisionError:
        ari = 1

    ari = ceil(ari)
    ari = max(ari, 1)
    ari = min(ari, 14)
    statistics["ari"] = ari

    ari_table = ["Kindergarten", "First grade", "Second grade",
                 "Third grade", "Fourth grade", "Fifth grade",
                 "Sixth grade", "Seventh grade", "Eighth grade",
                 "Ninth grade", "Tenth grade", "Eleventh grade",
                 "Twelfth grade", "College"]
    ari_grade_level = ari_table[ari-1]
    statistics["ari_grade_level"] = ari_grade_level
    ari_age_lower = ari + 4
    if ari_age_lower == 18:
        ari_age_upper = 22
    else:
        ari_age_upper = ari_age_lower + 1
    statistics["ari_age_lower"] = ari_age_lower
    statistics["ari_age_upper"] = ari_age_upper
    ari_age_lower = str(ari_age_lower)
    ari_age_upper = str(ari_age_upper)
    ari_age_range = "%s -- %s" % (ari_age_lower, ari_age_upper)
    statistics["ari_age_range"] = ari_age_range

    # sentiment
    pos, neg = get_sentiment(words)
    sentiment = (pos-neg)/len(words)
    statistics["sentiment"] = sentiment

    return statistics
