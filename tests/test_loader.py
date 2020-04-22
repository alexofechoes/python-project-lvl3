# -*- coding:utf-8 -*-
import logging
import os
import tempfile

import pytest
import requests
import requests_mock

import pageloader
from pageloader import loader

logger = logging.getLogger('pageloader')

_RESOURCE_URL = 'https://test.test/user/test/main-page/'


def test_save_url(simple_page_content): # noqa WPS210
    with requests_mock.Mocker() as mock:
        mock.get(_RESOURCE_URL, text=simple_page_content)

        with tempfile.TemporaryDirectory() as tmpdirname:
            empty_dir = os.listdir(tmpdirname)
            assert len(empty_dir) == 0

            loader.load(_RESOURCE_URL, tmpdirname)
            assert len(os.listdir(tmpdirname)) != 0

            files_path = [
                os.path.join(tmpdirname, file_name)
                for file_name in os.listdir(tmpdirname)
            ]
            with open(files_path[0], 'r') as file_descriptor:
                file_content = file_descriptor.read()
                assert file_content == simple_page_content


def test_save_url_with_fetch_exception():
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(loader.LoaderError):
            loader.load(_RESOURCE_URL, tmpdirname)


def test_save_url_with_tmpdir_err(simple_page_content):
    with requests_mock.Mocker() as mock:
        mock.get(_RESOURCE_URL, text=simple_page_content)
        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(loader.LoaderError):
                fake_dir = '{tmpdir}_fake_34213'.format(tmpdir=tmpdirname)
                loader.load(_RESOURCE_URL, fake_dir)


_expected_links = {
    '/assets/js/main.js': 'assets-js-main.js',
    '/css/styles.css': 'css-styles.css',
    '/image.png': 'image.png',
}


def test_get_resource_links(page_with_links_content):
    resource_dir_name = 'test-resource-dir_files'

    links_for_upload, replace_content = loader._get_resource_links(
        page_with_links_content, resource_dir_name,
    )

    assert _expected_links == links_for_upload
    for path in links_for_upload.values():
        expected_link = '{dir}/{path}'.format(dir=resource_dir_name, path=path)
        assert expected_link in replace_content


@pytest.mark.parametrize(
    'link,expected',
    [
        ('/assets/main.js', True),
        ('/assets/styles.css', True),
        ('/static/logo.png', True),
        ('https://cdn2.domain.io/dist.js', False),
        ('/user/info', False),
        ('', False),
        (' ', False),
    ],
)
def test_is_downloadable_resource(link, expected):
    result = loader._is_downloadable_resource(link)
    assert result == expected
