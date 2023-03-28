#!/usr/bin/env python
# @File: nico/api.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:44:55 pm
import json
import random
import shutil
import uuid
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

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    # TODO: implement __eq__ comparison between all keys of dict
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

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


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
        if self.validate_file(self.path):  # TODO change to is_valid_file
            self.load()  # Remove for lazy object creation
        else:
            print(f"{self.path} is not a valid genemede file")

    @staticmethod
    def read(fpath):
        with open(fpath, "r") as f:
            return json.load(f)

    @staticmethod
    def write(fpath, data):
        fpath = Path(fpath)
        if fpath.exists():
            EntityFile.backup(fpath)

        with open(fpath, "w") as f:
            json.dump([d for d in data], f, indent=4)

    @staticmethod
    def backup(fpath):
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

    @staticmethod
    def validate_file(fpath):  # XXX: fpath or data for staticmethod?
        """Checks if the json file is a valied gnmd file i.e.:
        - it's a list of dicts
        - dicts all have the same keys
        - all the keys match
        - all keys match the Entity template
        If ifle is validadated it can be safely opened as an EntityFile to Entity objects

        TODO: add capacity to check first dict being different from others
        """
        # Read the file
        data = EntityFile.read(fpath)
        # Check that it is a list of dicts
        assert isinstance(data, list), f"EntityFile.read({fpath}) <- not a list"
        assert all(
            [isinstance(d, dict) for d in data]
        ), f"EntityFile.read({fpath}) <- not a list of dicts"
        # select a random item to match to all the others
        random_item = random.choice(data)
        # Check if same number of keys (Entity level)
        assert all(
            [len(d) == len(random_item) for d in data]
        ), f"EntityFile.read({fpath}) <- not a list of dicts with same length"
        # Check if item keys are all the same
        assert all(
            [all([k in d.keys() for k in random_item.keys()]) for d in data]
        ), f"EntityFile.read({fpath}) <- not a list of dicts with same keys"
        # Check if item keys are the same as the template
        assert all(
            [all([k in Entity.template.keys() for k in d]) for d in data]
        ), f"EntityFile.read({fpath}) <- not a list of dicts with same keys"
        # Check if all template keys are in the item keys (use the random_item)
        assert all(
            [k in random_item.keys() for k in Entity.template.keys()]
        ), f"EntityFile.read({fpath}) <- some Entity template keys seem to be missing"

        return True

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
                if not bool(e.guid):
                    print(
                        f"EntityFile.fix_guids({self.path.name}): Will create GUID for  {e.name} -> current: {e.guid}"
                    )
                elif not isinstance(e.guid, str):
                    print(
                        f"EntityFile.fix_guids({self.path.name}): Will create GUID for {e.name} -> current: {e.guid}"
                    )
        else:
            for e in self.ents:
                if not bool(e.guid):
                    e.guid = str(uuid.uuid4())
                    print(
                        f"EntityFile.fix_guids({self.path.name}): Created GUID for {e.name} -> {e.guid}"
                    )
                elif not isinstance(e.guid, str):
                    e.guid = str(uuid.uuid4())
                    print(
                        f"EntityFile.fix_guids({self.path.name}): Created GUID for {e.name} -> {e.guid}"
                    )
            EntityFile.write(self.path, self.ents)

    def load(self):
        data = EntityFile.read(self.path)
        for d in data:
            self.ents.append(Entity(item=d))

    def save(self):
        EntityFile.write(self.path, self.ents)

    def update(self, data):
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
    root_path = Path("../tests/fixtures/metadata_databases/")
    fpath = root_path.joinpath("labs.json")
    bla = Entity()
    bla = [Entity() for _ in range(10)]
    EntityFile.write("./DELETEME.json", bla)
    fpath.exists()
    blaf = EntityFile(fpath)
    EntityFile.write("./DELETEME.json", blaf.ents)
    print(bla)
    print(blaf)
    print(0)
