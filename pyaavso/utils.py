from __future__ import unicode_literals

import logging
import requests

from .parsers import WebObsResultsParser


logger = logging.getLogger(__name__)

WEBOBS_RESULTS_URL = 'http://www.aavso.org/apps/webobs/results/'


def download_observations(observer_code):
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
        parser = WebObsResultsParser(response.content)
        observations.extend(parser.get_observations())
        if '>Next</a>' not in response.content:
            break
        page_number += 1
    return observations
