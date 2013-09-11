.. pyaavso documentation master file, created by
   sphinx-quickstart on Fri Aug 30 22:12:51 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======
pyaavso
=======

**pyaavso** is a Python library for working with
`AAVSO <http://www.aavso.org>`_ (American Association of Variable Star
Observers) data. The library is compatible with both Python 2.7 and 3.3+.

Features
========

* reading and writing variable star observations in AAVSO's
  `Visual File Format`_
* downloading all observation data for a given observer

.. _`Visual File Format`: http://www.aavso.org/aavso-visual-file-format


Installation
============

Use ``pip`` to install latest release available at PyPI::

    pip install pyaavso

Usage
=====

The following code uses :class:`~pyaavso.formats.visual.VisualFormatWriter`
to report a single observation of **SS Cyg** between the outbursts.

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

See :doc:`usage` for more examples.

Contents
========

.. toctree::
   :maxdepth: 4

   usage
   reference


License
=======

pyaavso is free software, licensed under the MIT/X11 License. A copy of
the license is provided with the source code in the LICENSE file.


Author
======

`Zbigniew Siciarz <http://siciarz.net>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

