#!/usr/bin/env python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def search(params):
    if 'hm' in params and params['hm'] != '*':
        return _parse(_fetch_reverse(params['hm']))

    return []

def _fetch_reverse(phone):
    URL = 'https://www.dasoertliche.de/Controller?form_name=search_inv&ph={}'
    with urllib.request.urlopen(URL.format(urllib.parse.quote(phone))) as resp:
        return resp.read()

def _parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    hits = soup.find_all('div', attrs={'class': 'hit'})
    results = []
    for hit in hits:
        result = {}
        result['ln'] = hit.a.text.strip()

        if result:
            results.append(result)

    return results
