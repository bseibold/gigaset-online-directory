#!/usr/bin/env python3

"""Backend for www.dasoertliche.de"""

import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup


def search(params):
    """Reverse search only"""

    if 'hm' in params and params['hm'] != '*':
        try:
            return _parse(_fetch_reverse(params['hm']))
        except urllib.error.URLError:
            return []
    return []


def _fetch_reverse(phone):
    url_base = 'https://www.dasoertliche.de/?form_name=search_inv&{}'
    url = url_base.format(urllib.parse.urlencode({'ph': phone}))
    with urllib.request.urlopen(url) as resp:
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
