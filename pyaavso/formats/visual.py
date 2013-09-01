from __future__ import unicode_literals

import csv

import pyaavso


class FormatException(Exception):
    """
    Raised when the data does not conform to AAVSO format specification.
    """


class VisualFormatWriter(object):
    """
    A class responsible for writing observation data in AAVSO
    `Visual File Format`_.

    The API here mimics the ``csv`` module in Python standard library.

    To write your observations into the data file, you first need to create
    the writer, passing to it the destination file and your observer code.
    Then call ``writerow()`` for every single observation, for example:

        >>> with open('data.txt', 'wb') as fp:
        ...     writer = VisualFormatWriter(fp, 'XYZ')
        ...     writer.writerow({
        ...         'name': 'SS CYG',
        ...         'date': '2450702.1234',
        ...         'magnitude': '<11.1',
        ...         'comment_code': 'na',
        ...         'comp1': '110',
        ...         'comp2': '113',
        ...         'chart': '070613',
        ...         'notes': 'This is a test',
        ...     })

    .. _`Visual File Format`: http://www.aavso.org/aavso-visual-file-format
    """

    def __init__(self, fp, observer_code, delimiter=str(','), date_format='JD',
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
            row = self.dict_to_row(observation_data)
        self.writer.writerow(row)

    def dict_to_row(self, observation_data):
        """
        Takes a dictionary of observation data and converts it to a list
        of fields according to AAVSO visual format specification.
        """
        row = []
        row.append(observation_data['name'])
        row.append(observation_data['date'])
        row.append(observation_data['magnitude'])
        row.append(observation_data['comment_code'])
        row.append(observation_data['comp1'])
        row.append(observation_data['comp2'])
        row.append(observation_data['chart'])
        row.append(observation_data['notes'])
        return row


class VisualFormatReader(object):
    """
    A class to read observations from file in AAVSO
    `Visual File Format`_.

    .. _`Visual File Format`: http://www.aavso.org/aavso-visual-file-format

    The reader API is also based on ``csv`` Python module. You create a reader
    instance by passing a file-like object in the constructor. This will
    read all the data and validate required headers. Then the reader object
    can be used to iterate over observation data.

    A short example:

        >>> with open('data.txt', 'rb') as fp:
        ...     reader = VisualFormatReader(fp)
        ...     for observation in reader:
        ...         print '%(name)s %(magnitude)s' % observation
        SS Cyg 10.0
        RZ Cas 6.4
    """

    def __init__(self, fp):
        """
        Creates the reader instance and reads file headers.

        Raises ``FormatException`` when any of the required headers could not
        be found in input. The following header parameters are required:

         * *TYPE* - always 'Visual', yet must be specified in file
         * *OBSCODE* - official AAVSO-assigned observer code
         * *DATE* - date format, must be one of 'JD' or 'Excel'

        Other headers described in AAVSO specification have reasonable default
        values, eg. the default delimiter is a comma, when not specified
        in headers. Without the *OBSTYPE* header, observations are assumed
        to be visual.
        """
        headers = {}
        data = []
        for line in fp:
            line = line.strip()
            if line and line[0] == '#' and '=' in line:
                header_str = line[1:]
                key, value = header_str.split('=', 1)
                headers[key] = value
            elif line and line[0] != '#':
                data.append(line)
        if 'TYPE' not in headers:
            raise FormatException('TYPE parameter is required')
        try:
            self.observer_code = headers['OBSCODE']
        except KeyError:
            raise FormatException('OBSCODE parameter is required')
        try:
            self.date_format = headers['DATE']
        except KeyError:
            raise FormatException('DATE parameter is required')
        self.software = headers.get('SOFTWARE', '')
        self.delimiter = str(headers.get('DELIM', ','))
        self.obstype = headers.get('OBSTYPE', 'Visual')
        self.reader = csv.reader(data, delimiter=self.delimiter)

    def __iter__(self):
        for row in self.reader:
            yield self.row_to_dict(row)

    def row_to_dict(self, row):
        """
        Converts a raw input record to a dictionary of observation data.
        """
        return {
            'name': row[0],
            'date': row[1],
            'magnitude': row[2],
            'comment_code': row[3],
            'comp1': row[4],
            'comp2': row[5],
            'chart': row[6],
            'notes': row[7],
        }
