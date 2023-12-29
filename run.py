#!/usr/bin/env python3

"""
Runner for debug purposes only.
Please use a proper WSGI server when deploying this.

This is intended as a more convenient alternative to
`flask run`, since environment variables cannot be easily
passed there.
"""

import os

os.environ["GIGASET_SETTINGS"] = "../settings.py"
import gigaset  # noqa: E402

if __name__ == "__main__":
    gigaset.app.debug = True
    gigaset.app.run(port=12345)
