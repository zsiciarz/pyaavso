from __future__ import unicode_literals

import unittest
from StringIO import StringIO

from pyaavso.formats.visual import VisualFormatWriter


class VisualFormatWriterTestCase(unittest.TestCase):
    """
    Tests for VisualFormatWriter class.
    """
    def test_write_header_obscode(self):
        """
        Check that observer code is written into file.
        """
        fp = StringIO()
        writer = VisualFormatWriter(fp, 'XYZ')
        contents = fp.getvalue()
        self.assertIn("#OBSCODE=XYZ", contents)
