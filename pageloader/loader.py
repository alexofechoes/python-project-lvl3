# -*- coding:utf-8 -*-

"""Module with requests."""
import os

import requests

from pageloader.helpers import get_file_name_from_url


def save_page_content(url: str, path_to_save_dir: str, save_func=None):
    """Save page content from url."""
    page_content = load_page_content(url)
    file_name = get_file_name_from_url(url)
    path_to_save = os.path.join(path_to_save_dir, file_name)

    if save_func is None:
        save_func = _save_to_file
    save_func(page_content, path_to_save)


def load_page_content(url: str) -> str:
    """Load and page content."""
    response = requests.get(url)
    return response.text


def _save_to_file(content_for_save: str, path_to_save: str):
    with open(path_to_save, 'w') as file_descriptor:
        file_descriptor.write(content_for_save)
