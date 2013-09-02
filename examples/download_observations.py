from __future__ import unicode_literals, print_function

import sys
import logging

from pyaavso.utils import download_observations


if __name__ == '__main__':
    # configure logging so we can see some informational output
    logger = logging.getLogger('pyaavso.utils')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    try:
        observer_code = sys.argv[1]
    except IndexError:
        print('Usage: python download_observations.py <OBSERVER_CODE>')
    else:
        observations = download_observations(observer_code)
        print('All done.\nDownloaded %d observations.' % len(observations))
