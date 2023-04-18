#!/usr/bin/env python
# @File: genemede/io.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Tuesday, April 18th 2023, 9:54:41 am

# Implement generic CRUD functions for *.gnmd files

import json
import random
import shutil
import typing as t
from datetime import datetime
from pathlib import Path
from genemede.core import Entity


def create(fpath: t.Union[str, Path], data: t.Union[list[dict], list[Entity]]) -> None:
    """Create genemede file from data.

    Args:
        fpath (t.Union[str, t.Path]): filepath to genemede file
        data (t.Union[list[t.dict], list[Entity]]): list of dicts or list of Entity objects
    """
    fpath = Path(fpath)
    # If fpath is folder,ask for name
    if fpath.is_dir():
        print("Warning: fpath is folder -> creating a new file with same name")
        fpath.joinpath(fpath.name + ".gnmd").mkdir(parents=True, exist_ok=True)

    # If fpath extension is not 'gnmd', change it to gnmd
    if fpath.suffix != ".gnmd":
        fpath = fpath.with_suffix(".gnmd")

    if fpath.exists():
        raise FileExistsError(f"{fpath} already exists")
        return

    with open(fpath, "w") as f:
        json.dump(data, f, indent=4)


def read(fpath: t.Union[str, Path]) -> None:
    with open(fpath, "r") as f:
        return json.load(f)


def update(fpath: t.Union[str, Path], data):
    """Backup exisiting file, delete it and create a new one with same name and the new data."""
    fpath = Path(fpath)
    if not fpath.exists():
        raise FileNotFoundError(f"{fpath} does not exist")
        return

    backup(fpath)

    # If fpath extension is not 'gnmd', change it to gnmd
    if fpath.suffix != ".gnmd":
        print("Warning: fpath extension is not '.gnmd' -> changing extension to '.gnmd'")
        fpath = fpath.with_suffix(".gnmd")

    with open(fpath, "w") as f:
        json.dump(data, f, indent=4)

    fpath = Path(fpath)
    with open(fpath, "w") as f:
        json.dump(data, f, indent=4)


def backup(fpath: t.Union[str, Path]) -> None:
    """Backup fpath by copying it and appending _bak_datetime

    Args:
        fpath (str or Path): path to genemede file
    """
    fpath = Path(fpath)
    fpath_bak = fpath.parent.joinpath(
        fpath.stem + "_bak_" + datetime.now().strftime("%Y-%m-%dT%H_%M_%S.%f") + fpath.suffix
    )
    fpath_bak.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(fpath, fpath_bak)


def is_valid_file(fpath):
    """Checks if the json file is a valied gnmd file i.e.:
    - it's a list of dicts
    - dicts all have the same keys
    - all the keys match
    - all keys match the Entity template
    If ifle is validadated it can be safely opened as an EntityFile to Entity objects

    TODO: add capacity to check first dict being different from others
    """
    # Read the file
    data = read(fpath)
    # Check that it is a list of dicts
    assert isinstance(data, list), f"genemede.io.read({fpath}) <- not a list"
    assert all(
        [isinstance(d, dict) for d in data]
    ), f"genemede.io.read({fpath}) <- not a list of dicts"
    # select a random item to match to all the others
    random_item = random.choice(data)
    # Check if same number of keys (Entity level)
    assert all(
        [len(d) == len(random_item) for d in data]
    ), f"genemede.io.read({fpath}) <- not a list of dicts with same length"
    # Check if item keys are all the same
    assert all(
        [all([k in d.keys() for k in random_item.keys()]) for d in data]
    ), f"genemede.io.read({fpath}) <- not a list of dicts with same keys"
    # Check if item keys are the same as the template
    assert all(
        [all([k in Entity.template.keys() for k in d]) for d in data]
    ), f"genemede.io.read({fpath}) <- not a list of dicts with same keys"
    # Check if all template keys are in the item keys (use the random_item)
    assert all(
        [k in random_item.keys() for k in Entity.template.keys()]
    ), f"genemede.io.read({fpath}) <- some Entity template keys seem to be missing"

    return True
