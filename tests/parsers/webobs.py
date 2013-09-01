from __future__ import unicode_literals

import unittest

from pyaavso.parsers.webobs import WebObsResultsParser


# this is a simplified actual HTML code from WebObs results page
RESULTS_HTML = """
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
<table class='observations'>
  <thead>
    <tr>
      <th><input type='checkbox' id='checkall'/></th>
      <th class='empty' colspan='2'></th>
      <th>Star</th>
      <th>JD</th>
      <th>Calendar Date</th>
      <th>Magnitude</th>
      <th>Error</th>
      <th>Filter</th>
      <th>Observer</th>
      <th class='empty' id='expand-all'></th>
    </tr>
  </thead>
  <tbody>
    <tr class='obs tr-even' id='ob-0'>
  <td><input type='checkbox' name='select-1263099015' class='obscheck' /></td>
  <td style='padding-right: 3px; padding-left: 5px;'>
    <a href='/webobs/edit/1263099015'>Edit</a>
  </td>
  <td style='padding-right: 5px; padding-left: 3px;'>
    <a href='/webobs/delete/1263099015'>Delete</a>
  </td>
  <td>NOVA DEL 2013</td>
  <td>2456529.3194</td>
  <td>2013 Aug. 24.81940</td>
  <td><a target='_blank' href='/lcg/plot?star=NOVA+DEL+2013&amp;height=450&amp;visual=on&amp;grid=on&amp;bband=on&amp;auid=000-BLC-933&amp;end=2456629.3194&amp;uband=on&amp;width=600&amp;obstotals=on&amp;start=2456429.3194&amp;v=on&amp;obscode=SYF'
      >5.9</a></td>
  <td>&mdash;</td>
  <td>Vis.</td>
  <td>SYF</td>
  <td><a href='#' class='obs-link' id='ob-0'>Details...</a>
  </td>
</tr>
<tr id='ob-0-detail' class='obs-detail-tr'>
  <td colspan='11'>
    <div id='ob-0-detail-div' class='obs-detail-div'>
    <table class='obs-detail'>
      <thead>
        <tr>
          <th>Comp Star</th>
          <th>Check Star</th>
          <th>Transformed</th>
          <th>Chart</th>
          <th>Comment Codes</th>
          <th>Notes</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>57
            </td>
          <td>61
            </td>
          <td>No</td>
          <td>12582DRJ</td>
          <td>&mdash;</td>
          <td>&mdash;</td>
        </tr>
      </tbody>
    </table>
    </div>
  </td>
</tr>
</table>
  </body>
</html>
"""


class WebObsResultsParserTestCase(unittest.TestCase):
    """
    Tests for WebObsResultsParser class.
    """
    def test_dummy(self):
        parser = WebObsResultsParser()
