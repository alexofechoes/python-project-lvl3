# -*- coding:utf-8 -*-

"""Module with helpers."""
import os
import re
from urllib.parse import urlparse


def get_file_name_from_url(url: str) -> str:
    """Get file name from url."""
    return '{name}.html'.format(name=_get_name_from_url(url))


def get_resource_name_from_url(resource_url: str) -> str:
    """Get resource name from url (static resource)."""
    [path, ext] = os.path.splitext(resource_url)
    return '{name}{ext}'.format(name=_get_name_from_url(path), ext=ext)


def get_resource_dir_name_from_url(url: str) -> str:
    """Get resource dir name from url."""
    return '{name}_files'.format(name=_get_name_from_url(url))


def _get_name_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    host = parsed_url.netloc.strip('/')
    path = parsed_url.path.strip('/')

    path_to = '/'.join(filter(lambda part: part, [host, path]))
    return re.sub(r'[^\w]+', '-', path_to)
