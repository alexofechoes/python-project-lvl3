# -*- coding:utf-8 -*-

"""Module with requests."""
import logging
import os
from typing import Union
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

    with Bar('Progress', max=len(links) + 2) as progress:
        logger.debug('Saving page')
        file_name = pageloader.url.to_filename(url)
        path_to_save_file = os.path.join(path_to_save_dir, file_name)
        _save_content(content_for_save, path_to_save_file)
        progress.next()

        logger.debug('Create resources directory')
        path_to_resources_dir = os.path.join(
            path_to_save_dir,
            resource_dir_name,
        )
        _create_resources_directory(path_to_resources_dir)
        progress.next()

        logger.debug('Saving resources')
        _download_resources(
            links,
            url,
            path_to_resources_dir,
            on_progress=progress.next,
        )


def _save_content(content_for_save: Union[str, bytes], path_to_file: str):
    try:
        storage.save(content_for_save, path_to_file)
    except OSError as save_err:
        logger.error('Save error: {err}'.format(
            err=save_err,
        ))
        raise LoaderError() from save_err


def _create_resources_directory(path_to_resource_dir: str):
    try:
        storage.create_dir(path_to_resource_dir)
    except OSError as create_dir_err:
        logger.error(
            'Create resource dir error: {err}'.format(
                err=create_dir_err,
            ),
        )
        raise LoaderError() from create_dir_err


def _download_resources(  # noqa WPS211
    links,
    base_url: str,
    path_to_resources_dir: str,
    on_progress=lambda: None, # noqa WPS404
):
    for link, name_for_save in links.items():
        file_content = _fetch_content(urljoin(base_url, link))
        path_to_file = os.path.join(path_to_resources_dir, name_for_save)
        _save_content(file_content, path_to_file)
        on_progress()


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


TAG_URL_ATTRIBUTES = [ # noqa WPS407
    ('script', 'src'),
    ('link', 'href'),
    ('img', 'src'),
]


def _get_resource_links(page_content, resource_dir_name): # noqa WPS210
    """Find resource links."""
    soup = BeautifulSoup(page_content, 'html.parser')

    links = {}
    for tag, attr in TAG_URL_ATTRIBUTES:
        for node in soup.find_all(tag):
            link = node.get(attr)
            if need_to_be_downloaded(link):
                resource_path = pageloader.url.to_resource(link)
                node[attr] = '{dir}/{path}'.format(
                    dir=resource_dir_name,
                    path=resource_path,
                )
                links[link] = resource_path

    return links, str(soup)


def need_to_be_downloaded(link: str) -> bool:
    """Check needable downloaded resource."""
    if link is None:
        return False
    return link.startswith('/') and os.path.splitext(link)[-1] != ''


class LoaderError(Exception):
    """Base class for exceptions in this module."""
