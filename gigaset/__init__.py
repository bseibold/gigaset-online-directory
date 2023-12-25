#!/usr/bin/env python3

"""Gigaset phonebook webapp"""

from importlib import import_module
import concurrent.futures
from flask import Flask

__version__ = "0.1"

app = Flask(__name__)
app.config.from_envvar('GIGASET_SETTINGS')

if app.debug:
    app.logger.setLevel(logging.DEBUG)

app.logger.debug(app.config)

backends = [import_module(name) for name in app.config['BACKENDS']]
executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(backends))


class Gigaset:
    """Helper class for the web app"""

    @staticmethod
    def _fix_phone(phone):
        """Normalize phone number"""
        
        # normalize phone number

        # add area code if it is missing    
        if phone[0] != '0' and phone[0] != '+':
            app.logger.debug("Adding missing areacode")
            phone = app.config['AREACODE'] + phone

        try:
            pn = phonenumbers.parse(phone, region=app.config["COUNTRY"])
        except phonenumbers.NumberParseException as e:
            app.logger.debug("Phone number {} not valid".format(phone))
            return phone

                
        app.logger.debug("Parsed number: {}".format(pn))
        
        phone = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
       
                
        return phone

    @staticmethod
    def search(**params):
        """Dispatch search requests to backends"""

        requests = []
        results = []

        
        if 'hm' in params:            

            app.logger.debug("searching phone number: {}".format(params['hm'])) 
            params['hm'] = Gigaset._fix_phone(params['hm'])
            app.logger.debug("normalized phone number: {}".format(params['hm'])) 

        for mod in backends:
            req = executor.submit(mod.search, params)
            requests.append(req)

        concurrent.futures.wait(requests, timeout=5)

        for req in requests:
            try:
                if req.done():
                    app.logger.debug("Request Done: {}".format(req.result()))
                    results += req.result()
            except:
                if app.config['DEBUG']:
                    raise

        app.logger.debug("results: {}".format(results)) 
                   
        return results


from . import views
