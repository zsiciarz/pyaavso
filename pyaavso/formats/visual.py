from __future__ import unicode_literals

import pyaavso


class VisualFormatWriter(object):
    """
    A class responsible for writing observation data in AAVSO
    `Visual File Format`_.

    The API here mimics the ``csv`` module in Python standard library.

    .. _`Visual File Format`: http://www.aavso.org/aavso-visual-file-format
    """

    def __init__(self, fp, observer_code, delimiter=',', date_format='JD', obstype='Visual'):
        """
        Creates the writer which will write observations into the file-like
        object given in first parameter. The only other required parameter
        is the official AAVSO-assigned observer code.
        """
        self.observer_code = observer_code
        self.date_format = date_format
        self.obstype = obstype
        fp.write('#TYPE=Visual\n')
        fp.write('#OBSCODE=%s\n' % observer_code)
        fp.write("#SOFTWARE=pyaavso %s\n" % pyaavso.get_version())
