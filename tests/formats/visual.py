from __future__ import unicode_literals

import unittest
from StringIO import StringIO

import pyaavso
from pyaavso.formats.visual import VisualFormatWriter


class VisualFormatWriterTestCase(unittest.TestCase):
    """
    Tests for VisualFormatWriter class.
    """
    def setUp(self):
        self.fp = StringIO()

    def tearDown(self):
        self.fp.close()

    def test_write_header_type(self):
        """
        Check that TYPE parameter is always Visual.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#TYPE=Visual", contents)

    def test_write_header_obscode(self):
        """
        Check that observer code is written into file.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#OBSCODE=XYZ", contents)

    def test_write_header_software(self):
        """
        Check that the SOFTWARE parameter is correct.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#SOFTWARE=pyaavso %s" % pyaavso.get_version(), contents)

    def test_write_header_date(self):
        """
        Check that the DATE parameter represents date format used.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ', date_format='jd')
        contents = self.fp.getvalue()
        self.assertIn("#DATE=JD", contents)

    def test_write_header_obstype(self):
        """
        Check that OBSTYPE parameter is correctly set.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ', obstype='Visual')
        contents = self.fp.getvalue()
        self.assertIn("#OBSTYPE=Visual", contents)

    def test_write_header_obstype_ptg(self):
        """
        Check that OBSTYPE can be set to PTG (Photographic).
        """
        writer = VisualFormatWriter(self.fp, 'XYZ', obstype='PTG')
        contents = self.fp.getvalue()
        self.assertIn("#OBSTYPE=PTG", contents)
