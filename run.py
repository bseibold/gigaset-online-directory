#!/usr/bin/env python3

import os

os.environ["GIGASET_SETTINGS"] = "../settings.py"
import gigaset  # noqa: E402

if __name__ == "__main__":
    gigaset.app.debug = gigaset.app.config["DEBUG"]
    gigaset.app.run(host="0.0.0.0", port=gigaset.app.config["PORT"])
