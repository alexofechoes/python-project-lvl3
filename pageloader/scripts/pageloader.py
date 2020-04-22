# -*- coding:utf-8 -*-

"""Main cli script."""
import argparse
import logging
import sys

from pageloader import loader

LOGGER_FORMAT = '%(asctime)s %(message)s' # noqa WPS323
logging.basicConfig(format=LOGGER_FORMAT)
logger = logging.getLogger('pageloader')

parser = argparse.ArgumentParser(description='Page Loader')
parser.add_argument(
    '-o',
    '--output',
    dest='output_dir',
    default='.',
    help='set output dir (default current dir)',
)
parser.add_argument(
    '-l',
    '--loglevel',
    dest='loglevel',
    default='INFO',
    help='set logging level(default INFO)',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
)
parser.add_argument('url', metavar='URL')


def main():
    """Run cli."""
    args = parser.parse_args()
    logger.setLevel(args.loglevel)

    try:
        loader.load(
            args.url,
            args.output_dir,
        )
    except loader.LoaderError:
        logger.error('Page load errors')
        sys.exit(1)
    logger.warning('Page load success')


if __name__ == '__main__':
    main()
