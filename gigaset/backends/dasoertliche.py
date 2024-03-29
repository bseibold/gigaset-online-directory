#!/usr/bin/env python3

"""Backend for www.dasoertliche.de"""

import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup


def search(params):
    """Reverse search only"""

    if "hm" in params and params["hm"] != "*":
        try:
            phone = params["hm"].replace("+", "00")
            return _parse(_fetch_reverse(phone), phone)
        except urllib.error.URLError:
            return []
    return []


def _fetch_reverse(phone):
    url_base = "https://www.dasoertliche.de/?form_name=search_inv&{}"
    url = url_base.format(urllib.parse.urlencode({"ph": phone}))
    with urllib.request.urlopen(url) as resp:
        return resp.read()


def _parse(html, phone):
    soup = BeautifulSoup(html, "html.parser")
    hits = soup.find_all("div", attrs={"class": "hit"})

    results = []
    for hit in hits:
        result = {}
        result["ln"] = hit.a.text.strip()
        result["hm"] = phone

        if result:
            results.append(result)

    return results
