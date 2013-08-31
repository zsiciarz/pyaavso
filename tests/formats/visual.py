from __future__ import unicode_literals

import unittest
from six import StringIO

import pyaavso
from pyaavso.formats.visual import VisualFormatWriter, VisualFormatReader, \
    FormatException


class VisualFormatWriterTestCase(unittest.TestCase):
    """
    Tests for VisualFormatWriter class.
    """
    def setUp(self):
        self.fp = StringIO()

    def tearDown(self):
        self.fp.close()

    def test_header_type(self):
        """
        Check that TYPE parameter is always Visual.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#TYPE=Visual", contents)

    def test_header_obscode(self):
        """
        Check that observer code is written into file.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#OBSCODE=XYZ", contents)

    def test_header_software(self):
        """
        Check that the SOFTWARE parameter is correct.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#SOFTWARE=pyaavso %s" % pyaavso.get_version(), contents)

    def test_header_date(self):
        """
        Check that the DATE parameter represents date format used.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ', date_format='jd')
        contents = self.fp.getvalue()
        self.assertIn("#DATE=JD", contents)

    def test_header_obstype(self):
        """
        Check that OBSTYPE parameter is correctly set.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ', obstype='Visual')
        contents = self.fp.getvalue()
        self.assertIn("#OBSTYPE=Visual", contents)

    def test_header_obstype_ptg(self):
        """
        Check that OBSTYPE can be set to PTG (Photographic).
        """
        writer = VisualFormatWriter(self.fp, 'XYZ', obstype='PTG')
        contents = self.fp.getvalue()
        self.assertIn("#OBSTYPE=PTG", contents)

    def test_write_raw_data(self):
        """
        Check that writerow() can accept raw data record.
        """
        data = [
            'SS CYG', '2450702.1234', '<11.1', 'na', '110', '113', '070613',
            'This is a test',
        ]
        writer = VisualFormatWriter(self.fp, 'XYZ')
        writer.writerow(data)
        lines = self.fp.getvalue().splitlines()
        self.assertEqual(
            lines[5],
            "SS CYG,2450702.1234,<11.1,na,110,113,070613,This is a test"
        )

    def test_write_dict(self):
        """
        Check that dictionary of observation data can be written to file.
        """
        data = {
            'name': 'SS CYG',
            'date': '2450702.1234',
            'magnitude': '<11.1',
            'comment_code': 'na',
            'comp1': '110',
            'comp2': '113',
            'chart': '070613',
            'notes': 'This is a test',
        }
        writer = VisualFormatWriter(self.fp, 'XYZ')
        writer.writerow(data)
        lines = self.fp.getvalue().splitlines()
        self.assertEqual(
            lines[5],
            "SS CYG,2450702.1234,<11.1,na,110,113,070613,This is a test"
        )


class VisualFormatReaderTestCase(unittest.TestCase):
    """
    Tests for VisualFormatReader class.
    """
    def setUp(self):
        self.lines = [
            "#TYPE=VISUAL",
            "#OBSCODE=XYZ",
            "#SOFTWARE=Notepad",
            "#DELIM=,",
            "#DATE=JD",
            "#OBSTYPE=Visual",
            "SS CYG,2450702.1234,<11.1,na,110,113,070613,This is a test",
        ]
        self.fp = StringIO("\n".join(self.lines))

    def tearDown(self):
        self.fp.close()

    def _drop_header(self, header_name):
        self.fp = StringIO("\n".join(
            line for line in self.lines if header_name not in line
        ))

    def test_missing_type(self):
        """
        Check that a missing TYPE header raises an exception.
        """
        self._drop_header('TYPE')
        with self.assertRaises(FormatException):
            reader = VisualFormatReader(self.fp)

    def test_observer_code(self):
        """
        Check that observer code matches header information.
        """
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.observer_code, 'XYZ')

    def test_missing_observer_code(self):
        """
        Check that a missing OBSCODE header raises an exception.
        """
        self._drop_header('OBSCODE')
        with self.assertRaises(FormatException):
            reader = VisualFormatReader(self.fp)

    def test_date_format(self):
        """
        Check that the date format is read correctly.
        """
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.date_format, 'JD')

    def test_missing_date_format(self):
        """
        Check that a missing DATE header raises an exception.
        """
        self._drop_header('DATE')
        with self.assertRaises(FormatException):
            reader = VisualFormatReader(self.fp)

    def test_software(self):
        """
        Check that SOFTWARE header is read correctly.
        """
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.software, 'Notepad')

    def test_missing_software(self):
        """
        Check that SOFTWARE header is not required.
        """
        self._drop_header('SOFTWARE')
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.software, '')

    def test_delimiter(self):
        """
        Check that the delimiter character is read correctly.
        """
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.delimiter, str(','))

    def test_missing_delimiter(self):
        """
        Check that in case of missing delimiter, a comma is assumed.
        """
        self._drop_header('DELIM')
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.delimiter, str(','))

    def test_obstype(self):
        """
        Check that observation type matches data in header.
        """
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.obstype, str('Visual'))

    def test_missing_obstype(self):
        """
        Check that Visual is assumed obstype when OBSTYPE header is missing.
        """
        self._drop_header('OBSTYPE')
        reader = VisualFormatReader(self.fp)
        self.assertEqual(reader.obstype, 'Visual')

    def test_row_count(self):
        """
        Check that number of records in initial input file is exactly 1.
        """
        reader = VisualFormatReader(self.fp)
        rows = [row for row in reader]
        self.assertEqual(len(rows), 1)

    def test_row_count_duplicated(self):
        """
        Check that there are exactly 2 records after duplicating the last line.
        """
        # duplicate the last line
        self.lines.append(self.lines[-1])
        self.fp = StringIO("\n".join(self.lines))
        reader = VisualFormatReader(self.fp)
        rows = [row for row in reader]
        self.assertEqual(len(rows), 2)
