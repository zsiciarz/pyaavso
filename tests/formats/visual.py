from __future__ import unicode_literals

import unittest
from StringIO import StringIO

from pyaavso.formats.visual import VisualFormatWriter


class VisualFormatWriterTestCase(unittest.TestCase):
    """
    Tests for VisualFormatWriter class.
    """
    def setUp(self):
        self.fp = StringIO()

    def tearDown(self):
        self.fp.close()

    def test_write_header_obscode(self):
        """
        Check that observer code is written into file.
        """
        writer = VisualFormatWriter(self.fp, 'XYZ')
        contents = self.fp.getvalue()
        self.assertIn("#OBSCODE=XYZ", contents)
