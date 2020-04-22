# -*- coding:utf-8 -*-

import pytest

from pageloader import url


def test_to_filename():
    expected = 'hexlet-io-courses.html'
    result = url.to_filename('https://hexlet.io/courses')
    assert expected == result


def test_to_resource_dirname():
    expected = 'hexlet-io-courses_files'
    result = url.to_resource_dirname('https://hexlet.io/courses')
    assert expected == result


def test_to_resource():
    expected = 'assets-application.css'
    result = url.to_resource('/assets/application.css')
    assert expected == result
