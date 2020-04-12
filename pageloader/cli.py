# -*- coding:utf-8 -*-

"""Cli module."""
import argparse
import logging
import sys

from progress.bar import Bar

from pageloader.loader import Loader

LOGGER_FORMAT = '%(asctime)s %(message)s' # noqa WPS323
logging.basicConfig(format=LOGGER_FORMAT)


parser = argparse.ArgumentParser(description='Page Loader')
parser.add_argument(
    '-o',
    '--output',
    dest='OUTPUT_DIR',
    default='.',
    help='set output dir (default current dir)',
)
parser.add_argument(
    '-l',
    '--loglevel',
    dest='LOGLEVEL',
    default='WARNING',
    help='set logging level(default WARNING)',
)
parser.add_argument('url', metavar='URL')


def main():
    """Run cli."""
    args = parser.parse_args()

    logger = logging.getLogger('pageloader')
    logger.setLevel(args.LOGLEVEL)

    progress_bar = Bar('Progress', max=5)
    loader = Loader(logger, progress_bar)
    try:
        loader.load(args.url, args.OUTPUT_DIR)
    except Exception: # noqa DAR401
        print('Page load errors')
        sys.exit(1)
    finally:
        progress_bar.finish()
    print('Page load success')


if __name__ == '__main__':
    main()
