#!/usr/bin/env python3

"""Backend for www.dastelefonbuch.de"""

import re
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup

_RE_ADDRESS = re.compile(r'(.*), (\d{5}) (.*)')


def search(params):
    """Search or reverse search"""

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
            results = [r for r in results
                       if 'type' in r and r['type'] == params['type']]
            return results
        except urllib.error.HTTPError:
            raise
    return []


def _fetch(name, city):
    """Retrieve page for forward search"""

    url_base = 'https://www.dastelefonbuch.de/Suche?{}'
    url = url_base.format(urllib.parse.urlencode({'kw': name, 'ci': city}))
    with urllib.request.urlopen(url) as resp:
        return resp.read()


def _fetch_reverse(phone):
    """Retrieve page for reverse search"""

    url_base = 'https://www.dastelefonbuch.de/R%C3%BCckw%C3%A4rts-Suche/{}'
    url = url_base.format(urllib.parse.quote(phone))

    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read()
    except urllib.error.URLError:
            # catches 404 responses returned from dasoertliche.de
            return ""
    

def _clean(html):
    """Remove obfuscation from HTML"""

    for hide in html.find_all(class_='hide'):
        hide.clear()
    for nodisplay in html.find_all(attrs={'style': 'display:none'}):
        nodisplay.clear()
    return ''.join(html.stripped_strings)


def _parse_name(hit, result):
    name = hit.select_one('span[itemprop="name"]').text.strip()
    result['ln'] = name
    match = re.match(r'(.*?) (.*)', name)
    if ('type', 'yp') not in result.items() and match:
        (last, first) = re.match(r'(.*?) (.*)', name).group(1, 2)
        result['fn'] = first
        result['ln'] = last


def _parse_address(hit, result):
    address = hit.find('a', class_='addr')['title'].strip()
    (street, zipcode, city) = _RE_ADDRESS.match(address).group(1, 2, 3)
    result['st'] = street
    result['ct'] = city


def _parse_phone(hit, result):
    try:
        phones = hit.find_all('div', class_='nr')
        for phone in phones:
            phone_nr = _clean(phone.span)
            if 'icon_mobil' in phone.i['class']:
                result['mb'] = phone_nr
            elif 'icon_phone' in phone.i['class']:
                result['hm'] = phone_nr
    except:
        pass


def _parse(html):
    """Parse HTML for results"""

    soup = BeautifulSoup(html, 'html.parser')
    hits = soup.find_all('div', class_='entry')
    results = []

    for hit in hits:

        result = {}

        if hit.find('a', class_='linkedin_url'):
            continue

        if hit.attrs.get('itemtype') == 'http://schema.org/Organization':
            result['type'] = 'yp'
        elif hit.attrs.get('itemtype') == 'http://schema.org/Person':
            result['type'] = 'pb'
        else:
            continue


        _parse_name(hit, result)
        _parse_address(hit, result)
        _parse_phone(hit, result)

        if result:
            results.append(result)

    return results
