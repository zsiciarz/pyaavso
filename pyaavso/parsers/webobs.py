from __future__ import unicode_literals

from lxml import html


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
        root = html.fromstring(html_source)
        self.tbody = root.xpath('//table[@class="observations"]/tbody')[0]

    def get_observations(self):
        """
        Parses the HTML table into a list of dictionaries, each of which
        represents a single observation.
        """
        rows = list(self.tbody)
        observations = []
        for row_observation, row_details in zip(rows[::2], rows[1::2]):
            data = {}
            cells = row_observation.xpath('./td//text()[normalize-space()]')
            data['name'] = _clean_cell(cells[0])
            data['date'] = _clean_cell(cells[1])
            data['magnitude'] = _clean_cell(cells[3])
            data['obscode'] = _clean_cell(cells[6])
            cells = row_details.xpath('./td/div/table/tbody/tr/td//text()[normalize-space()]')
            data['comp1'] = _clean_cell(cells[0])
            data['chart'] = _clean_cell(cells[3]).replace('None', '')
            data['comment_code'] = _clean_cell(cells[4])
            data['notes'] = _clean_cell(cells[5])
            observations.append(data)
        return observations
