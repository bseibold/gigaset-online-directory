gigaset
=======

This packages is intended to be used with Gigaset DECT base stations that are
connected via Ethernet / IP. These base stations support lookup of phone
numbers using an online service. However, the only supported preinstalled
provider is currently (as of 2019-10) tel.search.ch.

The base stations support configuring a custom provider, but the format for
requests and responses cannot be configured. This package therefore interprets
requests from the base station and forwards them to configurable online
services. The `protocol specification`_ is available online.

Please note that the 'backend' providers contained in this package are only
intended as examples. It is your responsibility as a user of this package to
check if you are compliant with the terms of service of the respective phone
book provider.

If you would prefer a simpler implementation written in PHP, please check out
`tigerxy/OnlineTelefonbuch`_ on GitHub. There is also a good documentation on
how to configure the base station.

.. _protocol specification: https://teamwork.gigaset.com/gigawiki/display/GPPPO/Online+directory
.. _tigerxy/OnlineTelefonbuch: https://github.com/tigerxy/OnlineTelefonbuch

Setup
-----

Adjust the used backend providers and the area code in settings.py and deploy
the WSGI app. Make sure that the environment variable GIGASET_SETTINGS points
to a configuration file like settings.py.

After deployment, the app should be accessible via a browser. If you deployed
the app to http://www.example.com/gigaset, then configure
http://www.example.com/gigaset/search as the server address in the web config
interface of your gigaset base station.

Local Phonebook
-----
The 'local' backend option let's you maintain a list of phone numbers and display names. 
The local phonebook is a simple json file.

Known Issues
-----
The service of *Das Telefonbuch* is currently returning *403 Forbidden*. 