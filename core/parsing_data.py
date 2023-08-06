import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from itertools import chain
import re
from core.lemmatized_text import lemmatize_text

stop_domains = [
    "2gis",
    "aliexpress",
    "auto",
    "avito",
    "banki",
    "beru",
    "blizko",
    "cataloxy",
    "deal",
    "domclick",
    "ebay",
    "edadeal",
    "e-katalog",
    "hh",
    "instagram",
    "irecommend",
    "irr",
    "leroymerlin",
    "mvideo",
    "onliner",
    "otzovik",
    "ozon",
    "pandao",
    "price",
    "prodoctorov",
    "profi",
    "pulscen",
    "quto",
    "rambler",
    "regmarkets",
    "satom",
    "shop",
    "sravni",
    "tiu",
    "toshop",
    "wikipedia",
    "wildberries",
    "yandex",
    "yell",
    "zoon",
]



def check_domain(domain):
    pattern = r"\/\/(?:www\.)?(\w+)"
    res = re.findall(pattern, domain)
    if res:
        return res[0]
    return None


def google_search(query, num=10):
    api_key = "AIzaSyBknCrYYm7uOS514Vq2C9jYNfZwCA6uK10"
    search_engine_id = "c6aed1893289f4d3a"

    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}&num={num}"
    response = requests.get(url).json()

    urls = []
    for i, item in enumerate(response["items"], 1):
        urls.append(item["link"])
    return urls


def yandex_search(query):
    url = f"http://xmlproxy.ru/search/xml?query={query}&groupby=attr%3Dd.mode%3Ddeep.groups-on-page%3D10.docs-in-group%3D1&maxpassages=3&page=1&user=rgvaramadze%40bk.ru&key=MTY1MjQ2MTMzODIyNDM1NzMxODQxODcwMDE0"
    response = requests.get(url).content

    root = ET.fromstring(response)
    urls = []

    for group in root.findall(".//group"):
        doc = group.find(".//doc/url")
        if doc is not None:
            urls.append(doc.text)

    return urls[:10]


def parse_data(query):
    urls1 = google_search(query)
    urls2 = yandex_search(query)
    res = set(chain(urls1, urls2))
    filtered_res = []
    for url in res:
        domain = check_domain(url)
        if domain and domain not in stop_domains:
            try:
                html = requests.get(url).content.decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')

                title = soup.title.string.replace('\n', ' ') if soup.title else "No title found"
                description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={
                    'name': 'description'}) else "No description found"
                h1 = soup.h1.string if soup.h1 else "No h1 tag found"
                text = lemmatize_text(soup.get_text())
                filtered_res.append({url: {"title": title, "description": description, "h1": h1, "text": text}})
            except Exception as e:
                pass
    return filtered_res
