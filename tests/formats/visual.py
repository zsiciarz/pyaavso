from __future__ import unicode_literals

import unittest

from pyaavso.formats.visual import VisualFormatWriter


class VisualFormatWriterTestCase(unittest.TestCase):
    def test_writer_init(self):
        writer = VisualFormatWriter()
