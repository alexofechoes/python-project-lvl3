# -*- coding:utf-8 -*-
"""Parsers module."""
import os

from bs4 import BeautifulSoup

_TAGS_WITH_LINK_ATTR = {  # noqa WPS407 (Found mutable module constant???)
    'script': 'src',
    'link': 'href',
    'img': 'src',
}


def parse_page_content(page_content, resource_dir_name, name_mapping_func): # noqa WPS210
    """Parse page content and return replace content and links for upload."""
    soup = BeautifulSoup(page_content, 'html.parser')

    links_for_upload = {}
    for tag in _TAGS_WITH_LINK_ATTR.keys():
        for node in soup.find_all(tag):
            link = node.get(_TAGS_WITH_LINK_ATTR[tag])

            is_download_resourse = (
                link and link.startswith('/') and os.path.splitext(link)[-1]
            )
            if (is_download_resourse):
                replace_path = name_mapping_func(link)
                node[_TAGS_WITH_LINK_ATTR[tag]] = '{dir}/{path}'.format(
                    dir=resource_dir_name,
                    path=replace_path,
                )
                links_for_upload[link] = replace_path

    return links_for_upload, str(soup)
