#!/usr/bin/env python
# @File: genemede/__init__.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Wednesday, October 12th 2022, 4:20:56 pm
__version__ = "0.0.1"
from pathlib import Path

test_path = Path(__file__).parent.parent.joinpath("tests")
from genemede.core import *
