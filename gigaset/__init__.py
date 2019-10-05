#!/usr/bin/env python3

from flask import Flask
import concurrent.futures
from importlib import import_module

app = Flask(__name__)
app.config.from_envvar('GIGASET_SETTINGS')

backends = [import_module(name)  for name in app.config['BACKENDS']]
executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(backends))

class Gigaset:
    @staticmethod
    def _fix_phone(phone):
        if phone[0] != '0' and phone[0] != '+':
            return app.config['AREACODE'] + phone
        return phone

    @staticmethod
    def search(**params):
        requests = []
        results = []

        if 'phone' in params:
            params['phone'] = Gigaset._fix_phone(params[phone])

        for mod in backends:
            req = executor.submit(mod.search, params)
            requests.append(req)

        concurrent.futures.wait(requests, timeout=5)

        for req in requests:
            try:
                if req.done():
                    results += req.result()
            except:
                if app.config['DEBUG'] == True:
                    raise

        return results

from . import views

