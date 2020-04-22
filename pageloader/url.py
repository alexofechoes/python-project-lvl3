# -*- coding:utf-8 -*-

"""Module with helpers."""
import os
import re
from urllib.parse import urlparse


def to_filename(url: str) -> str:
    """Get file name from url."""
    return '{name}.html'.format(name=_get_name_from_url(url))


def to_resource(resource_url: str) -> str:
    """Get resource name from url (static resource)."""
    path, ext = os.path.splitext(resource_url)
    return '{name}{ext}'.format(name=_get_name_from_url(path), ext=ext)


def to_resource_dirname(url: str) -> str:
    """Get resource dir name from url."""
    return '{name}_files'.format(name=_get_name_from_url(url))


def _get_name_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    host = parsed_url.netloc.strip('/')
    path = parsed_url.path.strip('/')

    path_to = os.path.join(host, path)
    return re.sub(r'[^\w]+', '-', path_to)
