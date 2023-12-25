#!/usr/bin/env python3

"""Backend for www.dasoertliche.de"""

import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
#debug only: import sys

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
    #print(url, file=sys.stderr)
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read()
    except urllib.error.URLError:
            # catches 404 responses returned from dasoertliche.de
            return ""


def _parse(html, phone):
    soup = BeautifulSoup(html, 'html.parser')
    hits = soup.find_all('div', attrs={'class': 'hit'})
    # for new interface 
    #hits = soup.find_all('div', attrs={'class': 'name'})
    
    #print(hits, file=sys.stderr)
    results = []
    for hit in hits:
        result = {}
        result['ln'] = hit.a.text.strip()
        # for new interface 
        #result['ln'] = hit.h1.text.strip()
        result["hm"] = phone

        if result:
            results.append(result)

    #print (results, file=sys.stderr)
    return results
