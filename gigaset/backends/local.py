#!/usr/bin/env python3

"""Backend for local json store"""

import json


def search(params):
    """Reverse search only"""

    results = []

    if "hm" in params and params["hm"] != "*":
        with open("local.json") as json_file:
            db = json.load(json_file)

            match = next((d for d in db if params["hm"] in d["number"]), None)

            if match:
                found = {}
                found["ln"] = match["last_name"]
                found["fn"] = match["first_name"]
                found["hm"] = params["hm"]
                results.append(found)

    return results
