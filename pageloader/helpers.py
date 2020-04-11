# -*- coding:utf-8 -*-

"""Module with helpers."""
import re
from urllib.parse import urlparse


def get_file_name_from_url(url: str) -> str:
    """Get file name from url.

    Without protocol and replace all not word symbols.
    """
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path
    path_without_first_slash = '' if path == '/' else path

    return '{host}{path}.html'.format(
        host=_replace_path(host),
        path=_replace_path(path_without_first_slash),
    )


def _replace_path(string: str) -> str:
    return re.sub(r'[^\w]+', '-', string)
