# -*- coding:utf-8 -*-
import logging
import os
import tempfile

import pytest
import requests
import requests_mock

from pageloader.loader import Loader

logger = logging.getLogger(__name__)


def test_save_url(): # noqa WPS210
    url = 'https://test.test/user/test/main-page/'
    content = _get_content_data()

    with requests_mock.Mocker() as mock:
        mock.get(url, text=content)

        with tempfile.TemporaryDirectory() as tmpdirname:
            empty_dir = os.listdir(tmpdirname)
            assert len(empty_dir) == 0

            loader = Loader(logger)
            loader.load(url, tmpdirname)
            assert len(os.listdir(tmpdirname)) != 0

            files_path = [
                os.path.join(tmpdirname, file_name)
                for file_name in os.listdir(tmpdirname)
            ]
            with open(files_path[0], 'r') as file_descriptor:
                file_content = file_descriptor.read()
                assert file_content == content


def test_save_url_with_fetch_exception():
    url = 'https://test.test/user/test/main-page/'
    with tempfile.TemporaryDirectory() as tmpdirname:
        with pytest.raises(requests.exceptions.RequestException):
            loader = Loader(logger)
            loader.load(url, tmpdirname)


def test_save_url_with_tmpdir_err():
    url = 'https://test.test/user/test/main-page/'

    with requests_mock.Mocker() as mock:
        mock.get(url, text=_get_content_data())
        with tempfile.TemporaryDirectory() as tmpdirname:
            with pytest.raises(FileNotFoundError):
                loader = Loader(logger)
                fake_dir = '{tmpdir}_fake_34213'.format(tmpdir=tmpdirname)
                loader.load(url, fake_dir)


def _get_content_data():
    return """
<!DOCTYPE html>

<html lang="ru">
<head>
<title>test test</title>
</head>
<body>
<p>test content</p>
</body>
</html>"""
