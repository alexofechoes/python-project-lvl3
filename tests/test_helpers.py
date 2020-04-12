# -*- coding:utf-8 -*-

import pytest

from pageloader import helpers


def test_get_file_name_from_url():
    expected = 'hexlet-io-courses.html'
    result = helpers.get_file_name_from_url('https://hexlet.io/courses')
    assert expected == result


def test_get_resource_dir_name_from_url():
    expected = 'hexlet-io-courses_files'
    result = helpers.get_resource_dir_name_from_url('https://hexlet.io/courses')
    assert expected == result


def test_get_resource_name_from_url():
    expected = 'assets-application.css'
    result = helpers.get_resource_name_from_url('/assets/application.css')
    assert expected == result
