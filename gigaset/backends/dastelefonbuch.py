#!/usr/bin/env python3

import re
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup

_re_address = re.compile(r'(.*), (\d{5}) (.*)')

def search(params):
    if 'hm' in params and params['hm'] != '*':
        phone = params['hm']
        try:
            return _parse(_fetch_reverse(phone))
        except urllib.error.HTTPError:
            return []
    else:
        if 'type' in params and params['type'] == 'yp':
            name = params['wh']
        else:
            name = params['ln']
        city = params['ct']

        try:
            html = _fetch(name, city)
            results = _parse(html)
            results = [r for r in results if 'type' in r and r['type'] == params['type']]
            return results
        except urllib.error.HTTPError:
            raise
    return []

def _fetch(name, city):
    URL = 'https://www.dastelefonbuch.de/Suche?kw={}&ci={}'
    url = URL.format(urllib.parse.quote(name), urllib.parse.quote(city))
    with urllib.request.urlopen(url) as resp:
        return resp.read()

def _fetch_reverse(phone):
    URL = 'https://www.dastelefonbuch.de/R%C3%BCckw%C3%A4rts-Suche/{}'
    with urllib.request.urlopen(URL.format(urllib.parse.quote(phone))) as resp:
        return resp.read()

def _clean(html):
    for hide in html.find_all(attrs={'class': 'hide'}):
        hide.clear()
    for nodisplay in html.find_all(attrs={'style': 'display:none'}):
        nodisplay.clear()
    return ''.join(html.stripped_strings)

def _parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    hits = soup.find_all('div', attrs={'class': 'entry'})
    results = []
    for hit in hits:

        if hit.find('a', attrs={'class': 'linkedin_url'}):
            continue

        result = {}

        try:
            if hit['itemtype'] == 'http://schema.org/Organization':
                result['type'] = 'yp'
            elif hit['itemtype'] == 'http://schema.org/Person':
                result['type'] = 'pb'
        except:
            pass

        try:
            name = hit.find('span', attrs={'itemprop': 'name'}).text.strip()
            match = re.match(r'(.*?) (.*)', name)
            if not ('type', 'yp') in result.items() and match:
                (last, first) = re.match(r'(.*?) (.*)', name).group(1,2)
                result['fn'] = first
                result['ln'] = last
            else:
                result['ln'] = name

        except:
            pass

        try:
            address = hit.find('a', attrs={'class': 'addr'})['title'].strip()
            (street, zipcode, city) = _re_address.match(address).group(1, 2, 3)
            result['st'] = street
            result['ct'] = city
        except:
            pass
            
        try:
            phones = hit.find_all('div', attrs={'class': 'nr'})
            hm = None
            mb = None
            for phone in phones:
                phone_nr = _clean(phone.span)
                if 'icon_mobil' in phone.i['class']:
                    mb = phone_nr
                elif 'icon_phone' in phone.i['class']:
                    hm = phone_nr
            if hm:
                result['hm'] = hm
            if mb:
                result['mb'] = mb
        except:
            pass

        if result:
            results.append(result)

    return results
