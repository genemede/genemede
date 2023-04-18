#!/usr/bin/env python
# @File: nico/api.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:44:55 pm
import json
import shutil
import uuid
import genemede.io as io
from datetime import datetime
from pathlib import Path


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
        if item is None:
            for k in self.template:
                self.__dict__.update({k: None})
        else:
            self.from_dict(item)
        # Add automatic GUID generation and datetime timestamp
        if self.guid is None:
            self.guid = str(uuid.uuid4())
        if self.datetime is None:
            self.datetime = datetime.now().isoformat()

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def from_dict(self, item):
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
        if squeeze:
            return {k: v for k, v in self.__dict__.items() if v is not None}
        else:
            return {k: v for k, v in self.__dict__.items()}


# ADD Create Read Update and Delete methods
class EntityFile(object):
    """EntityFile is a class that stores a list of GNMD entities and allows to
    add, update, and delete entities.
    Implements a series of checks to ensure that the entity is valid before
    storing it in the database.

    Args:
        path (str): Path to a json/gnmd file.
    """

    def __init__(self, path):
        self.path = Path(path)
        self.ents = []
        if io.is_valid_file(self.path):  # TODO change to is_valid_file
            self.load()  # Remove for lazy object creation
        else:
            print(f"{self.path} is not a valid genemede file")

    def check_guids(self) -> bool:
        """Checks if all the entities have guids and if they are valid
        uuid.uuid4()"""
        has_something = all([bool(d.guid) for d in self.ents])
        if not has_something:
            print(f"EntityFile.check_guids({self.path.name}) <- not all entities have guids")
            return False
        are_strings = all([isinstance(d.guid, str) for d in self.ents])
        if not are_strings:
            print(f"EntityFile.check_guids({self.path.name}) <- not all entities have guids")
            return False
        try:
            for d in self.ents:
                uuid.UUID(d.guid)
        except BaseException as e:
            print(e)
            print(f"EntityFile.check_guids({self.path.name}) <- not all guids are uuid.UUID")
            return False

        return True

    def fix_guids(self, dry_run=True):
        """Fixes the guids of all the entities in the EntityFile

        Args:
            dry_run (bool, optional): Do everything except changing the values. Defaults to True.
        """
        if dry_run:
            for e in self.ents:
                # Check if guid is valid
                try:
                    uuid.UUID(e.guid)
                except BaseException as x:
                    print(
                        f"EntityFile.fix_guids({self.path.name}): Will create GUID for {e.name} -> current: {e.guid}"
                    )
        else:
            for e in self.ents:
                # Fix invalid guids
                try:
                    uuid.UUID(e.guid)
                except BaseException as x:
                    e.guid = str(uuid.uuid4())
                    print(
                        f"EntityFile.fix_guids({self.path.name}): Created GUID for {e.name} -> {e.guid}"
                    )

            EntityFile.write(self.path, self.ents)

    def fix_datetimes(self, dry_run=True):
        """Fixes the datetimes of all the entities in the EntityFile"""
        if dry_run:
            for e in self.ents:
                # Check if datetime is valid
                try:
                    datetime.strptime(e.datetime, "%Y-%m-%dT%H:%M:%S.%f")
                except BaseException as x:
                    print(
                        f"EntityFile.fix_datetimes({self.path.name}): Will create datetime for {e.name} -> current: {e.datetime}"
                    )
        else:
            for e in self.ents:
                # Fix invalid datetimes
                try:
                    datetime.strptime(e.datetime, "%Y-%m-%dT%H:%M:%S.%f")
                except BaseException as x:
                    e.datetime = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
                    print(
                        f"EntityFile.fix_datetimes({self.path.name}): Created datetime for {e.name} -> {e.datetime}"
                    )
            EntityFile.write(self.path, self.ents)

    def load(self):
        data = EntityFile.read(self.path)
        for d in data:
            self.ents.append(Entity(item=d))

    def save(self):
        EntityFile.write(self.path, self.ents)

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


if __name__ == "__main__":
    import genemede as gm

    fpath = gm.test_path.joinpath("fixtures/metadata_descriptors/labs/labs.json")
    labs = EntityFile(fpath)
    labs.fix_guids(False)
    print(0)
