# -*- coding:utf-8 -*-

import pytest

from pageloader import helpers


def test_get_file_name_from_url():
    expected = 'hexlet-io-courses.html'
    result = helpers.get_file_name_from_url('https://hexlet.io/courses')
    assert expected == result
