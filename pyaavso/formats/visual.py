from __future__ import unicode_literals

import csv

import pyaavso


class VisualFormatWriter(object):
    """
    A class responsible for writing observation data in AAVSO
    `Visual File Format`_.

    The API here mimics the ``csv`` module in Python standard library.

    .. _`Visual File Format`: http://www.aavso.org/aavso-visual-file-format
    """

    def __init__(self, fp, observer_code, delimiter=b',', date_format='JD',
                 obstype='Visual'):
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
        fp.write("#DATE=%s\n" % date_format.upper())
        fp.write("#OBSTYPE=%s\n" % obstype)
        self.writer = csv.writer(fp, delimiter=delimiter)

    def writerow(self, observation_data):
        """
        Writes a single observation to the output file.

        If the ``observation_data`` parameter is a dictionary, it is
        converted to a list to keep a consisted field order (as described
        in format specification). Otherwise it is assumed that the data
        is a raw record ready to be written to file.
        """
        if isinstance(observation_data, (list, tuple)):
            row = observation_data
        else:
            row = []
            row.append(observation_data['name'])
            row.append(observation_data['date'])
            row.append(observation_data['magnitude'])
            row.append(observation_data['comment_code'])
            row.append(observation_data['comp1'])
            row.append(observation_data['comp2'])
            row.append(observation_data['chart'])
            row.append(observation_data['notes'])
        self.writer.writerow(row)
