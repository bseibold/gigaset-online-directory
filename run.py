#!/usr/bin/env python3

import gigaset

if __name__ == '__main__':
    gigaset.app.debug = True
    gigaset.app.run(host='0.0.0.0', port=12345)
