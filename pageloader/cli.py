# -*- coding:utf-8 -*-

"""Cli module."""
import argparse
import logging

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

    loader = Loader(logger)
    try:
        loader.load(args.url, args.OUTPUT_DIR)
        print('Page load success')
    except Exception: # noqa DAR401
        print('Page load errors')


if __name__ == '__main__':
    main()
