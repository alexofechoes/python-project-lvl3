# -*- coding:utf-8 -*-

"""Cli module."""
import argparse

from pageloader import loader

parser = argparse.ArgumentParser(description='Page Loader')
parser.add_argument(
    '-o',
    '--output',
    dest='OUTPUT_DIR',
    default='.',
    help='set output dir',
)
parser.add_argument('url', metavar='URL')


def main():
    """Run cli."""
    args = parser.parse_args()
    loader.save_page_content(args.url, args.OUTPUT_DIR)


if __name__ == '__main__':
    main()
