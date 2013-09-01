from __future__ import unicode_literals

from lxml import html


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
            data['name'] = cells[0].replace('\u2014', '').strip()
            data['date'] = cells[1]
            data['magnitude'] = cells[3]
            data['obscode'] = cells[6]
            cells = row_details.xpath('./td/div/table/tbody/tr/td//text()[normalize-space()]')
            data['comp1'] = cells[0].replace('\u2014', '').strip()
            data['chart'] = cells[3].replace('None', '').replace('\u2014', '').strip()
            data['comment_code'] = cells[4].replace('\u2014', '').strip()
            data['notes'] = cells[5].replace('\u2014', '').strip()
            observations.append(data)
        return observations
