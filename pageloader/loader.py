# -*- coding:utf-8 -*-
"""Module with requests."""
import os
from urllib.parse import urljoin

import requests

from pageloader import helpers, parsers


def save_page_content(url: str, path_to_save_dir: str, save_func=None): # noqa WPS210
    """Save page content from url."""
    page_content = _fetch_content(url)

    resource_dir_name = helpers.get_resource_dir_name_from_url(url)
    file_name = helpers.get_file_name_from_url(url)
    path_to_resource_dir = os.path.join(path_to_save_dir, resource_dir_name)

    links, content_for_save = parsers.parse_page_content(
        page_content,
        resource_dir_name,
        helpers.get_resource_name_from_url,
    )

    path_to_save_file = os.path.join(path_to_save_dir, file_name)

    if save_func is None:
        save_func = _save_to_file
    save_func(content_for_save, path_to_save_file)

    if not os.path.exists(path_to_resource_dir):
        os.mkdir(path_to_resource_dir)

    for link, name_for_save in links.items():
        resource_url = urljoin(url, link)
        file_content = _fetch_content(resource_url)

        path_to_file = os.path.join(path_to_resource_dir, name_for_save)
        save_func(file_content, path_to_file)


def _fetch_page(url: str):
    """Load content."""
    response = requests.get(url)
    return response.text


def _fetch_content(url: str):
    response = requests.get(url)
    return response.content


def _save_to_file(content_for_save, path_to_save: str):
    mode = 'w' if isinstance(content_for_save, str) else 'wb'
    with open(path_to_save, mode) as file_descriptor:
        file_descriptor.write(content_for_save)
