cosmicpi-protocol
=================

.. image:: https://img.shields.io/pypi/v/cosmicpi-protocol.svg
    :target: https://pypi.python.org/pypi/cosmicpi-protocol
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/CosmicPi/cosmicpi-protocol.png
   :target: https://travis-ci.org/CosmicPi/cosmicpi-protocol
   :alt: Latest Travis CI build status

Parser for data read from Arduino.

Usage
-----

Open a console and execute::

  $ echo '1,DAT,20161212' | cosmicpi-protocol
  ["protocol-v1.0:date", {"date": "20161210"}]

Installation
------------

Clone this repository and run `pip install -e .`

Authors
-------

`cosmicpi-protocol` was written by `Jiri Kuncar <jiri.kuncar@gmail.com>`_.
