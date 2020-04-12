# -*- coding:utf-8 -*-
"""Module with requests."""
import os
from urllib.parse import urljoin

import requests

from pageloader import helpers, parsers
from pageloader.saver import FileSaver


class Loader:
    """Page loader."""

    def __init__(self, logger, progress=None, saver=None, fetch_func=None):  # noqa D107
        self.logger = logger
        self.progress = progress or FakeProgress
        self.saver = saver or FileSaver()
        self.fetch_func = fetch_func or _fetch_content

    def __call__(self, url: str, path_to_save_dir: str):
        """Save page with resources from url."""
        self.load(url)

    def load(self, url: str, path_to_save_dir: str): # noqa WPS213
        """Save page with resources from url."""
        self.progress.next()
        self.logger.info('Fetching page content')

        page_content = self.fetch_func(url, self.logger)
        resource_dir_name = helpers.get_resource_dir_name_from_url(url)

        self.progress.next()
        self.logger.debug('Start search resources on page')
        try:
            links, content_for_save = parsers.parse_page_content(
                page_content,
                resource_dir_name,
                helpers.get_resource_name_from_url,
            )
        except Exception as parse_err:
            self.logger.error('Parse resource page err: {err}'.format(
                err=str(parse_err),
            ))
            raise parse_err

        self.progress.next()
        self.logger.info('Saving page')
        file_name = helpers.get_file_name_from_url(url)
        self._save_page_content(file_name, path_to_save_dir, content_for_save)

        self.progress.next()
        self.logger.info('Saving resources')
        self._load_and_save_page_resources(
            links, url, path_to_save_dir, resource_dir_name,
        )

        self.progress.next()

    def _save_page_content(
        self, file_name: str, path_to_save_dir: str, page_content: str,
    ):
        path_to_save_file = os.path.join(path_to_save_dir, file_name)
        try:
            self.saver.save(page_content, path_to_save_file)
        except OSError as save_page_err:
            self.logger.critical('Save page error: {err}'.format(
                err=save_page_err,
            ))
            raise save_page_err

    def _load_and_save_page_resources(
        self,
        links_for_upload,
        base_url: str,
        path_to_save_dir: str,
        resource_dir_name: str,
    ):
        path_to_resource_dir = os.path.join(path_to_save_dir, resource_dir_name)
        try:
            self.saver.create_dir(path_to_resource_dir)
        except OSError as create_dir_err:
            self.logger.critical('Create resource dir error: {err}'.format(
                err=create_dir_err,
            ))
            raise create_dir_err

        for link, name_for_save in links_for_upload.items():
            file_content = self.fetch_func(urljoin(base_url, link), self.logger)
            path_to_file = os.path.join(path_to_resource_dir, name_for_save)

            try:
                self.saver.save(file_content, path_to_file)
            except OSError as save_resource_err:
                self.logger.error('Saving resource error: {err}'.format(
                    err=save_resource_err,
                ))
                raise save_resource_err


def _fetch_content(url: str, logger) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as fetch_err:
        logger.critical('Fetch resource {url} error: {err}'.format(
            url=url,
            err=fetch_err,
        ))
        raise fetch_err
    return response.content


class FakeProgress: # noqa
    @staticmethod # noqa
    def next(): # noqa
        return None
