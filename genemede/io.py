#!/usr/bin/env python
# @File: genemede/io.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Tuesday, April 18th 2023, 9:54:41 am

# Implement generic CRUD functions for *.gnmd files

import json
import shutil
import typing as t
from datetime import datetime
from pathlib import Path

# TODO: Consider adding a .gnmd folder to user home directory to store genemede files and backups


def create(fpath: t.Union[str, Path], data: list[dict]) -> None:
    """
    Creates a new file with the given file path and writes the given data to it in JSON format.

    Args:
        fpath (Union[str, Path]): The path of the file to create.
        data (list[dict]): The data to write to the file in JSON format.

    Raises:
        FileExistsError: If the file already exists at the given path.

    Returns:
        None
    """
    fpath = Path(fpath)
    # If fpath is folder, ask for name
    if fpath.is_dir():
        print(f"Warning: {fpath} is folder -> creating a new file with same name")
        fpath.joinpath(fpath.name + ".gnmd").mkdir(parents=True, exist_ok=True)

    # If fpath extension is not 'gnmd', change it to gnmd
    if fpath.suffix != ".gnmd":
        print(f"Warning: {fpath} extension is not '.gnmd' -> changing extension to '.gnmd'")
        fpath = fpath.with_suffix(".gnmd")

    if fpath.exists():
        raise FileExistsError(f"{fpath} already exists")
        return

    with open(fpath, "w") as f:
        json.dump(data, f, indent=4)


def read(fpath: t.Union[str, Path]) -> ...:
    """
    Read a JSON file and return its contents as a Python object.

    Args:
        fpath: A string or Path object representing the path of the file to read.

    Returns:
        The Python object resulting from loading the JSON file's contents.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        JSONDecodeError: If the file does not contain valid JSON data.
        UnicodeDecodeError: If the file is not encoded in UTF-8.
    """
    with open(fpath, "r") as f:
        return json.load(f)


def backup(fpath: t.Union[str, Path]) -> None:
    """Backup fpath by copying it and appending _bak_datetime

    This function creates a backup of a file by copying it and appending the
    current date and time to its name. The backup file is saved in the same
    directory as the original file.

    Args:
        fpath (str or Path): The path to the file to be backed up.

    Returns:
        None
    """
    fpath = Path(fpath)
    fpath_bak = fpath.parent.joinpath(
        fpath.stem + "_bak_" + datetime.now().strftime("%Y-%m-%dT%H_%M_%S.%f") + fpath.suffix
    )
    fpath_bak.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(fpath, fpath_bak)


def update(fpath: t.Union[Path, str], data):
    """
    Update the file at the given path with the given data, creating a backup
    first.

    Args:
        fpath: the path of the file to update
        data: the data to write to the file

    Raises:
        FileNotFoundError: if the file at the given path does not exist

    Returns:
        None
    """
    if not fpath.exists():
        raise FileNotFoundError(f"{fpath} does not exist")
        return
    delete(fpath)
    create(fpath, data)


def delete(fpath: t.Union[str, Path]) -> None:
    """
    Delete the file at the given path, after making a backup copy.

    Args:
        fpath (Union[str, Path]): The path to the file to delete.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.

    Returns:
        None
    """
    fpath = Path(fpath)
    if not fpath.exists():
        raise FileNotFoundError(f"{fpath} does not exist")
        return
    backup(fpath)
    fpath.unlink()
