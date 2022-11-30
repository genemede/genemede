#!/usr/bin/env python
# @File: tests/test_package.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Tuesday, October 18th 2022, 11:44:10 am
import pytest
from pkg_resources import parse_version


def test_version():
    try:
        import genemede as gm
    except BaseException as e:
        pytest.raises(e, pytrace=True)
    assert isinstance(gm.__version__, str)


def test_version_casting():
    try:
        import genemede as gm
    except BaseException as e:
        pytest.raises(e, pytrace=True)

    gm.__version__
