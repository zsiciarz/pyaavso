=======
pyaavso
=======

.. image:: https://requires.io/github/zsiciarz/pyaavso/requirements.svg?branch=master
    :target: https://requires.io/github/zsiciarz/pyaavso/requirements/?branch=master
    :alt: Requirements Status

.. image:: https://img.shields.io/pypi/v/pyaavso.svg
    :target: https://pypi.python.org/pypi/pyaavso/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/pyaavso.svg
    :target: https://pypi.python.org/pypi/pyaavso/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/pyversions/pyaavso.svg
    :target: https://pypi.python.org/pypi/pyaavso/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/pyaavso.svg
    :target: https://pypi.python.org/pypi/pyaavso/
    :alt: Wheel Status

.. image:: https://travis-ci.org/zsiciarz/pyaavso.svg?branch=master
    :target: https://travis-ci.org/zsiciarz/pyaavso

.. image:: https://coveralls.io/repos/zsiciarz/pyaavso/badge.svg?branch=master
    :target: https://coveralls.io/r/zsiciarz/pyaavso?branch=master

**pyaavso** is a Python library for working with
`AAVSO <http://www.aavso.org>`_ (American Association of Variable Star
Observers) data. The library is compatible with both Python 2.7 and 3.3+.

Features
--------

* reading and writing variable star observations in AAVSO's
  `Visual File Format`_
* downloading all observation data for a given observer

.. _`Visual File Format`: http://www.aavso.org/aavso-visual-file-format

Installation
------------

Use ``pip`` to install latest release available at PyPI::

    pip install pyaavso

Usage
-----

The following code uses ``VisualFormatWriter`` to report a single
observation of **SS Cyg** between the outbursts.

    >>> from pyaavso.formats import VisualFormatWriter
    >>> observer_code = 'XYZ'
    >>> with open('data.txt', 'wb') as fp:
    ...     writer = VisualFormatWriter(fp, observer_code)
    ...     writer.writerow({
    ...         'name': 'SS CYG',
    ...         'date': '2450702.1234',
    ...         'magnitude': '<11.0',
    ...         'comp1': '110',
    ...         'chart': '070613',
    ...     })

The ``data.txt`` file can be now submitted to AAVSO.

Resources
---------

 * `Documentation <http://pyaavso.rtfd.org>`_
 * `Issue tracker <https://github.com/zsiciarz/pyaavso/issues>`_
 * `CI server <https://travis-ci.org/zsiciarz/pyaavso>`_

Author
------

 * `Zbigniew Siciarz <http://siciarz.net>`_ (zbigniew at siciarz dot net)

License
-------

pyaavso is free software, licensed under the MIT/X11 License. A copy of
the license is provided with the source code in the LICENSE file.
