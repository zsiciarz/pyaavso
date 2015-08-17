from lxml import html
from lxml.etree import XPath


TBODY_XPATH = XPath('//table[@class="observations"]/tbody')
OBSERVATION_XPATH = XPath('./td//text()[normalize-space()]')
DETAILS_XPATH = XPath('./td/div/table/tbody/tr/td//text()')


def _clean_cell(value):
    """
    Removes dashes and strips whitespace from the given value.
    """
    return value.replace('\u2014', '').strip()


class WebObsResultsParser(object):
    """
    Parser for WebObs search results page.

    The parser reads an HTML page with search results (presented as a table)
    and parses the table into a list of observations.
    """

    def __init__(self, html_source):
        """
        Creates the parser and feeds it source code of the page.
        """
        self.empty = "There were no results for this search." in html_source
        if not self.empty:
            root = html.fromstring(html_source)
            self.tbody = TBODY_XPATH(root)[0]

    def get_observations(self):
        """
        Parses the HTML table into a list of dictionaries, each of which
        represents a single observation.
        """
        if self.empty:
            return []
        rows = list(self.tbody)
        observations = []
        for row_observation, row_details in zip(rows[::2], rows[1::2]):
            data = {}
            cells = OBSERVATION_XPATH(row_observation)
            data['name'] = _clean_cell(cells[0])
            data['date'] = _clean_cell(cells[1])
            data['magnitude'] = _clean_cell(cells[3])
            data['obscode'] = _clean_cell(cells[6])
            cells = DETAILS_XPATH(row_details)
            data['comp1'] = _clean_cell(cells[0])
            data['chart'] = _clean_cell(cells[3]).replace('None', '')
            data['comment_code'] = _clean_cell(cells[4])
            data['notes'] = _clean_cell(cells[5])
            observations.append(data)
        return observations
