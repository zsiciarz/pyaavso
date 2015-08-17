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
      <th class='empty' colspan='3'></th>
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
  <td class='empty' colspan='3'></td>
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

EMPTY_RESULTS_HTML = """
<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
  <p>There were no results for this search.</p>
  </body>
</html>
"""


class WebObsResultsParserTestCase(unittest.TestCase):
    """
    Tests for WebObsResultsParser class.
    """

    def test_count_observations(self):
        """
        Check that get_observations() returns all observations from the page.
        """
        parser = WebObsResultsParser(RESULTS_HTML)
        observations = parser.get_observations()
        self.assertEqual(len(observations), 1)

    def test_observation_data(self):
        """
        Check that parsed observation data are valid and meaningful.
        """
        parser = WebObsResultsParser(RESULTS_HTML)
        observations = parser.get_observations()
        observation = observations[0]
        self.assertEqual(observation['name'], 'NOVA DEL 2013')
        self.assertEqual(observation['date'], '2456529.3194')
        self.assertEqual(observation['magnitude'], '5.9')
        self.assertEqual(observation['obscode'], 'SYF')
        self.assertEqual(observation['comp1'], '57')
        self.assertEqual(observation['chart'], '12582DRJ')
        self.assertEqual(observation['comment_code'], '')
        self.assertEqual(observation['notes'], '')

    def test_no_results(self):
        """
        Check that parser returns no observations for empty results page.
        """
        parser = WebObsResultsParser(EMPTY_RESULTS_HTML)
        observations = parser.get_observations()
        self.assertEqual(len(observations), 0)
