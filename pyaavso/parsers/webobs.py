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
