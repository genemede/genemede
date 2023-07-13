#!/usr/bin/env python
# @File: genemede/curate.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Thursday, June 15th 2023, 11:13:44 am


import uuid
from datetime import datetime
from pathlib import Path

import genemede as gnmd
from genemede import io


def fix_entity_missing_keys(data: list[dict]) -> list[dict]:
    """
    Fixes the missing keys in a list of dicts or entities.
    """
    for d in data:
        for ek in gnmd.Entity.template:
            if ek not in d:
                d[ek] = None

    return data


def fix_guids(data: list[dict]) -> list[dict]:
    """Fixes the guids of all the entities in the EntityFile

    Args:
        dry_run (bool, optional): Do everything except changing the values. Defaults to True.
    """
    for d in data:
        # Check if guid is valid
        try:
            uuid.UUID(d["guid"])
        except BaseException as x:
            d["guid"] = str(uuid.uuid4())
            # print(f"fix_guids(): Created GUID for {d["name"]} -> current: {d["guid"]}")
    return data


def fix_datetimes(data: list[dict]) -> list[dict]:
    """Fixes the datetimes of all the entities in the EntityFile"""
    for d in data:
        # Fix invalid datetimes
        try:
            datetime.strptime(d["datetime"], "%Y-%m-%dT%H:%M:%S.%f")
        except BaseException as x:
            d["datetime"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
            # print(f"fix_datetimes: Created datetime for {d["name"]} -> {d["datetime"]}" )
    return data


def fix_entity_missing_keys_file(fpath: Path) -> None:
    """
    Fixes the missing keys in a file.
    """
    data = io.read(fpath)
    fixed_data = fix_entity_missing_keys(data)
    io.update(fpath, fixed_data)


def try_fix_file(fpath: str | Path) -> None:
    """
    Tries to fix common issues with a file.
    """
    try:
        data = io.read(fpath)
        fixed_data = data[:]
    except BaseException as e:
        print("-->", fpath, "-->", e)
    try:
        fixed_data = fix_entity_missing_keys(data)
    except BaseException as e:
        print("-->", fpath, "-->", e)
    try:
        fixed_data = fix_guids(fixed_data)
    except BaseException as e:
        print("-->", fpath, "-->", e)
    try:
        fixed_data = fix_datetimes(fixed_data)
    except BaseException as e:
        print("-->", fpath, "-->", e)
    try:
        io.update(fpath, fixed_data)
    except BaseException as e:
        print("-->", fpath, "-->", e)


if __name__ == "__main__":
    fpath = "/home/nico/Projects/COGITATE/GENEMEDE/genemede/tests/fixtures/metadata_databases/devices.json"
    fpath = "/home/nico/Projects/COGITATE/GENEMEDE/genemede/tests/fixtures/metadata_descriptors/"
    files = gnmd.find_gnmd_files(fpath)
    print(files)
    for f in files:
        try:
            try_fix_file(f)
        except BaseException as e:
            print("-->", f, "-->", e)

    # gnmd.is_valid_file(fpath)
    # data = io.read(fpath)
    # fpath = gm.test_path.joinpath("fixtures/metadata_descriptors/labs/labs.json")
    # labs = EntityFile(fpath)
    # labs.fix_guids(False)
    print(0)
