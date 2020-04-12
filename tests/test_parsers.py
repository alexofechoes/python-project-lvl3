# -*- coding:utf-8 -*-
import pytest

from pageloader.helpers import get_resource_name_from_url
from pageloader import parsers


def test_get_links_for_upload():
    expected_links = {
        '/assets/js/main.js': 'assets-js-main.js',
        '/css/styles.css': 'css-styles.css',
        '/image.png': 'image.png',
    }
    resource_dir_name = 'test-resource-dir_files'

    links_for_upload, replace_content = parsers.parse_page_content(
        _get_content_data(), resource_dir_name, get_resource_name_from_url,
    )

    assert expected_links == links_for_upload
    for path in links_for_upload.values():
        expected_link = '{dir}/{path}'.format(dir=resource_dir_name, path=path)
        assert expected_link in replace_content


def _get_content_data():
    return """
    <!DOCTYPE html>
        <head>
            <title>test test</title>
            <link href="/css/styles.css" />
            <link href="http://bootstrap.com/main.css"/>
            <script src="/assets/js/main.js"></script>
            <script src="http://bootstrap.com/main.js"></script>
        </head>
        <body>
            <p>test content</p>
            <link href="/content" />
            <img src="/image.png">
            <img alt="/image.png">
            <div src="/broken.url">
                test content
            </div>
            <form action="/user/create" method="POST">
                <input type="text" name="username" />
                <input type="submit" value="submit" />
            </form>
        </body>
    </html>
    """
