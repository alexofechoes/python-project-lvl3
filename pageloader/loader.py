# -*- coding:utf-8 -*-
"""Module with requests."""
import os
from urllib.parse import urljoin

import requests

from pageloader import helpers, parsers


class Loader:
    """Page loader."""

    def __init__(self, logger, save_func=None, fetch_func=None):  # noqa D107
        self.logger = logger
        self.save_func = save_func or _save_to_file
        self.fetch_func = fetch_func or _fetch_content

    def __call__(self, url: str, path_to_save_dir: str):
        """Save page with resources from url."""
        self.load(url)

    def load(self, url: str, path_to_save_dir: str):
        """Save page with resources from url."""
        self.logger.info('fetching page content')
        page_content = self.fetch_func(url)
        resource_dir_name = helpers.get_resource_dir_name_from_url(url)

        self.logger.debug('start search resources on page')
        links, content_for_save = parsers.parse_page_content(
            page_content, resource_dir_name, helpers.get_resource_name_from_url,
        )

        self.logger.info('saving page')
        file_name = helpers.get_file_name_from_url(url)
        try:
            self._save_page_content(
                file_name, path_to_save_dir, content_for_save,
            )
        except Exception as file_save_err:
            self.logger.critical('saving page error: : {err}'.format(
                err=str(file_save_err),
            ))
            raise file_save_err

        try:
            self._load_and_save_page_resources(
                links, url, path_to_save_dir, resource_dir_name,
            )
        except Exception as resources_save_err:
            self.logger.critical('saving resources error: {err}'.format(
                err=str(resources_save_err),
            ))
            raise resources_save_err

    def _save_page_content(
        self, file_name: str, path_to_save_dir: str, page_content: str,
    ):
        path_to_save_file = os.path.join(path_to_save_dir, file_name)
        self.save_func(page_content, path_to_save_file)

    def _load_and_save_page_resources(
        self,
        links_for_upload,
        base_url: str,
        path_to_save_dir: str,
        resource_dir_name: str,
    ):
        path_to_resource_dir = os.path.join(path_to_save_dir, resource_dir_name)
        # extract create dir in saver object
        if not os.path.exists(path_to_resource_dir):
            os.mkdir(path_to_resource_dir)

        for link, name_for_save in links_for_upload.items():
            file_content = _fetch_content(urljoin(base_url, link))
            path_to_file = os.path.join(path_to_resource_dir, name_for_save)
            self.save_func(file_content, path_to_file)


def _fetch_content(url: str) -> bytes:
    response = requests.get(url)
    return response.content


def _save_to_file(content_for_save, path_to_save: str):
    mode = 'w' if isinstance(content_for_save, str) else 'wb'
    with open(path_to_save, mode) as file_descriptor:
        file_descriptor.write(content_for_save)
