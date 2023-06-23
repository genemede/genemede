#!/usr/bin/env python
# @File: nico/api.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:44:55 pm
import json
import random
import typing as t
import uuid
from datetime import datetime
from pathlib import Path

import genemede.io as io


class Entity(dict):
    template = {
        "guid": str,
        "datetime": str,
        "name": str,
        "description": str,
        "mtype": str,
        "resources": list,
        "properties": list,
        "custom": list,
        "bids": list,
    }

    def __init__(self, item=None):
        """
        Initialize a new instance of this class.

        Args:
            item (Optional[Dict[str, Any]]): An optional dictionary of attribute names and values to initialize with.
                If not passed, all attributes are initialized to `None`.

        Returns:
            None
        """
        if item is None:
            for k in self.template:
                self.__dict__.update({k: None})
        else:
            self.from_dict(item)
        # Add automatic GUID generation and datetime timestamp
        if not self.guid:
            self.guid = str(uuid.uuid4())
        if not self.datetime:
            self.datetime = datetime.now().isoformat()  # type: ignore

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def from_dict(self, item: dict) -> None:
        """
        Check if item is a dict, if any key in the item is not in the template
        and if all item keys are in the template. If no errors are raised the item
        matches the entity template, we can add the item's key value to the object's __dict__
        """
        if not isinstance(item, dict):
            raise TypeError(f"{item} <- not a dict")
        if any([k not in self.template for k in item.keys()]):
            raise KeyError(f"{item} <- does not match template")
        if not all([k in item.keys() for k in self.template.keys()]):
            raise KeyError(f"{item} <- does not match template")

        for k, v in item.items():
            self.__dict__.update({k: v})

    def to_dict(self, squeeze=True):
        """
        Converts the object's attributes to a dictionary.

        Args:
            squeeze (bool, optional): If True, only include non-None values in the dictionary.
                Defaults to True.

        Returns:
            dict: A dictionary of the object's attributes.
        """
        if squeeze:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        else:
            return {k: v for k, v in self.__dict__.items()}


class EntityFile(object):
    """EntityFile is a class that stores a list of GNMD entities and allows to
    add, update, and delete entities.
    Implements a series of checks to ensure that the entity is valid before
    storing it in the database.

    Args:
        path (str): Path to a json/gnmd file.
    """

    def __init__(self, path, lazy=False):
        self.path = Path(path)
        self.ents = []
        if not self.path.exists():
            print(f"Warning: {self.path} does not exist")
            return
        elif not is_valid_file(self.path):
            print(f"Error: {self.path} is not a valid genemede file")
        elif not lazy:
            self.load()

    def load(self):
        data = io.read(self.path)
        for d in data:
            self.ents.append(Entity(item=d))

    def save(self):
        io.create(self.path, self.ents)

    def update(self, data):  # Use EntityFile.write
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self):
        self.path.unlink()

    def exists(self):
        return self.path.exists()

    def __repr__(self):
        return str(self.path)

    def __str__(self):
        return str(self.path)


def is_valid_gnmd_struct(data: t.Union[list[dict], list[Entity]]) -> bool:
    """
    Check whether the given data is a valid GNMD structure.

    Args:
    - data: a list of either dictionaries or entities
      (i.e., instances of the `Entity` class).

    Returns:
    - A boolean indicating whether the data is valid, i.e.,
      whether it meets the following criteria:
      1. It is a list.
      2. All its elements are either dictionaries or entities.
      3. All its dictionaries/entities have the same set of keys.
      4. All its dictionaries/entities have the same number of keys.
      5. All its dictionaries/entities have the same keys as the `Entity.template`.
    """
    out = True
    # Check that it is a list of dicts
    if not isinstance(data, list):
        print(f"Error: The data is not a list")
        out = False
    if not (
        all([isinstance(d, dict) for d in data]) or all([isinstance(d, Entity) for d in data])
    ):
        print(f"Error: The data is not a list of dicts or a list of Entities")
        out = False
    random_item = random.choice(data)
    # Check if all dicts have the same number of keys
    if not all([len(d) == len(random_item) for d in data]):
        print(f"Error: The data is not a list of dicts with same length")
        out = False
    # and that they match
    if not all([all([k in d.keys() for k in random_item.keys()]) for d in data]):
        print(f"Error: The data is not a list of dicts with same keys")
        out = False
    # Now that they are all the 'same' we can check with the random_item keysmatch the template's
    if not len(random_item) == len(Entity.template):
        print(f"Error: The putative entity items are not the same length as the template")
        out = False
    if not all([k in Entity.template.keys() for k in random_item.keys()]):
        print(f"Error: Found unknown keys in putative entities")
        out = False
    if not all([k in random_item.keys() for k in Entity.template.keys()]):
        print(f"Error: Missing keys in putative entity")
        out = False
    return out


def is_valid_file(fpath):
    """Checks if the json file is a valied gnmd file i.e.:
    - it's a list of dicts
    - dicts all have the same keys
    - all the keys match
    - all keys match the Entity template
    If ifle is validadated it can be safely opened as an EntityFile to Entity objects

    TODO: add capacity to check first dict being different from others
    """
    data = io.read(fpath)
    if is_valid_gnmd_struct(data):
        return True
    else:
        print(f"Error: {fpath} is not a valid gnmd file")
        return False


def find_gnmd_files(path: t.Union[str, Path]) -> t.List[t.Union[str, Path]]:
    """
    Return a list of all .json files in the given path that are valid genemede files.

    Args:
        path (Union[str, Path]): The path to search for .gnmd files.

    Returns:
        A list of all .gnmd files in the given path.
    """
    path = Path(path)
    files = []
    for f in path.glob("*.json"):
        if is_valid_file(f):
            files.append(f)
    return files
