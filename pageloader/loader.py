# -*- coding:utf-8 -*-
"""Module with requests."""
import logging
import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup  # type: ignore
from progress.bar import Bar  # type: ignore

import pageloader.url  # noqa WPS301
from pageloader import storage

logger = logging.getLogger(__name__)


def load(url: str, path_to_save_dir: str):  # noqa WPS213
    """Save page with resources from url."""

    logger.info('Fetching page content')
    page_content = _fetch_content(url)
    resource_dir_name = pageloader.url.to_resource_dirname(url)

    logger.debug('Start search resources on page')
    links, content_for_save = _get_resource_links(
        page_content,
        resource_dir_name,
    )

    progress = Bar('Progress', max=len(links) + 2)

    progress.next()
    logger.debug('Saving page')
    file_name = pageloader.url.to_filename(url)
    _save_page_content(file_name, path_to_save_dir, content_for_save)

    progress.next()
    logger.debug('Saving resources')
    _load_and_save_page_resources(
        links,
        url,
        path_to_save_dir,
        resource_dir_name,
        progress=progress,
    )

    progress.finish()


def _save_page_content(
    file_name: str,
    path_to_save_dir: str,
    page_content: str,
):
    path_to_save_file = os.path.join(path_to_save_dir, file_name)
    try:
        storage.save(page_content, path_to_save_file)
    except OSError as save_page_err:
        logger.error('Save page error: {err}'.format(
            err=save_page_err,
        ))
        raise LoaderError() from save_page_err


def _load_and_save_page_resources(  # noqa WPS211
    links_for_upload,
    base_url: str,
    path_to_save_dir: str,
    resource_dir_name: str,
    progress,
):
    path_to_resource_dir = os.path.join(path_to_save_dir, resource_dir_name)
    try:
        storage.create_dir(path_to_resource_dir)
    except OSError as create_dir_err:
        logger.error(
            'Create resource dir error: {err}'.format(
                err=create_dir_err,
            ),
        )
        raise LoaderError() from create_dir_err

    for link, name_for_save in links_for_upload.items():
        file_content = _fetch_content(urljoin(base_url, link))
        path_to_file = os.path.join(path_to_resource_dir, name_for_save)
        progress.next()
        try:
            storage.save(file_content, path_to_file)
        except OSError as save_resource_err:
            logger.error(
                'Saving resource error: {err}'.format(
                    err=save_resource_err,
                ),
            )
            raise LoaderError() from save_resource_err


def _fetch_content(url: str) -> bytes:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as fetch_err:
        logger.error(
            'Fetch resource {url} error: {err}'.format(
                url=url,
                err=fetch_err,
            ),
        )
        raise LoaderError() from fetch_err
    return response.content


_tag2attr = [
    ('script', 'src'),
    ('link', 'href'),
    ('img', 'src'),
]


def _get_resource_links(page_content, resource_dir_name): # noqa WPS210
    """Find links for upload."""
    soup = BeautifulSoup(page_content, 'html.parser')

    links_for_upload = {}
    for tag, attr in _tag2attr:
        for node in soup.find_all(tag):
            link = node.get(attr)
            if _is_downloadable_resource(link):
                resource_path = pageloader.url.to_resource(link)
                node[attr] = '{dir}/{path}'.format(
                    dir=resource_dir_name,
                    path=resource_path,
                )
                links_for_upload[link] = resource_path

    return links_for_upload, str(soup)


def _is_downloadable_resource(link: str) -> bool:
    if not link:
        return False
    resource_extension = os.path.splitext(link)[-1]
    return link.startswith('/') and resource_extension != ''


class LoaderError(Exception):
    """Base class for exceptions in this module."""
