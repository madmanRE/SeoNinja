import string
import requests
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from pymystem3 import Mystem
from itertools import chain
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

m = Mystem()

stop_words = stopwords.words("russian") + stopwords.words("english")


def get_lems(text):
    text = re.sub(r'[\n\r\t"©«»]', " ", text)
    text = text.replace("  ", " ")
    text = re.sub(r"\s{1,}", " ", text)
    text = m.lemmatize(
        text.translate(str.maketrans("", "", string.punctuation)).lower()
    )
    text = [word for word in text if word not in stop_words]
    while " " in text:
        text.remove(" ")
    while "  " in text:
        text.remove("  ")
    text = set(text)
    return list(text)


def lemmatize_text(text):
    text = re.sub(r'[\n\r\t"©«»]', " ", text)
    text = text.replace("  ", " ")
    text = re.sub(r"\s{1,}", " ", text)
    text = m.lemmatize(
        text.translate(str.maketrans("", "", string.punctuation)).lower()
    )
    while " " in text:
        text.remove(" ")
    while "  " in text:
        text.remove("  ")
    l = len(text)
    filtered_words = [word for word in text if word not in stop_words]
    counter = Counter(filtered_words)
    cloud = WordCloud().generate(" ".join(filtered_words))
    image_path = "backend/static/img/wordcloud.jpg"
    cloud.to_file(image_path)
    words = [word for word, _ in counter.most_common(10)]
    frequencies = [counter[word] for word in words]
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies)
    plt.xticks(rotation=45)
    chart_path = "backend/static/img/word_frequencies_chart.jpg"
    plt.savefig(chart_path, format="jpg")
    plt.close()
    return [
        [word, counter[word], f"{round(counter[word] / l * 100, 2)}%"]
        for word, _ in counter.most_common(10)
    ]


def get_ngramms(text):
    text = re.sub(r"\d", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation)).lower()
    nltk_tokens = nltk.word_tokenize(text)
    bigrams = Counter(list(nltk.bigrams(nltk_tokens))).most_common(10)
    trigrams = Counter(list(nltk.trigrams(nltk_tokens))).most_common(10)
    return {"bigrams": bigrams, "trigrams": trigrams}


def parse_text(url=None, text=None):
    if url is not None and len(url) > 5:
        html = requests.get(url).content.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text()
        result = lemmatize_text(text)
        return {"lemmas": result, "ngrams": get_ngramms(text)}
    elif text is not None and len(text) > 300:
        result = lemmatize_text(text)
        return {"lemmas": result, "ngrams": get_ngramms(text)}



