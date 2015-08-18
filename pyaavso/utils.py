import logging

import requests

from .parsers import WebObsResultsParser


logger = logging.getLogger(__name__)

WEBOBS_RESULTS_URL = 'https://www.aavso.org/apps/webobs/results/'


def download_observations(observer_code):
    """
    Downloads all variable star observations by a given observer.

    Performs a series of HTTP requests to AAVSO's WebObs search and
    downloads the results page by page. Each page is then passed to
    :py:class:`~pyaavso.parsers.webobs.WebObsResultsParser` and parse results
    are added to the final observation list.
    """
    page_number = 1
    observations = []
    while True:
        logger.info('Downloading page %d...', page_number)
        response = requests.get(WEBOBS_RESULTS_URL, params={
            'obscode': observer_code,
            'num_results': 200,
            'obs_types': 'all',
            'page': page_number,
        })
        logger.debug(response.request.url)
        parser = WebObsResultsParser(response.text)
        observations.extend(parser.get_observations())
        # kinda silly, but there's no need for lxml machinery here
        if '>Next</a>' not in response.text:
            break
        page_number += 1
    return observations
