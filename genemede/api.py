#!/usr/bin/env python
# @File: nico/jsondb.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:44:55 pm
import json
import random
import uuid
from pathlib import Path
from pprint import pprint


class Entity:
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


class EntityFile(object):
    """EntityFile is a class that stores a list of GNMD entities and allows to
    add, update, and delete entities.
    Implements a series of checks to ensure that the entity is valid before
    storing it in the database.

    Args:
        object (_type_): _description_
    """

    def __init__(self, path):
        self.path = Path(path)
        self.ents = []
        self.load()  # Remove for lazy object creation

    @staticmethod
    def read(fpath):
        with open(fpath, "r") as f:
            return json.load(f)

    @staticmethod
    def write(fpath, data):
        with open(fpath, "w") as f:
            json.dump(data, f, indent=4)

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
        # Check if keys are the same
        assert all(
            [all([k in d.keys() for k in random_item.keys()]) for d in data]
        ), f"EntityFile.read({fpath}) <- not a list of dicts with same keys"
        # Check if keys are the same as the template
        assert all(
            [all([k in Entity.template.keys() for k in d]) for d in data]
        ), f"EntityFile.read({fpath}) <- not a list of dicts with same keys"

        return True

    def check_guids(self) -> bool:
        """Checks if all the entities have guids and if they are valid
        uuid.uuid4()"""
        has_something = all([bool(d.guid) for d in self.ents])
        if not has_something:
            print(f"EntityFile.check_guids({self.path}) <- not all entities have guids")
        are_strings = all([isinstance(d.guid, str) for d in self.ents])
        if not are_strings:
            print(f"EntityFile.check_guids({self.path}) <- not all entities have guids")
        try:
            for d in self.ents:
                uuid.UUID(d.guid)
        except ValueError as e:
            print(e)
            print(f"EntityFile.check_guids({self.path}) <- not all guids are uuid.UUID")

        return True

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


# class EntityDB:
#     def __init__(self, filename):
#         self.filename = filename
#         self.entities = []
#         self.load()

#     def load(self):
#         data = get_data(self.filename)
#         for item in data:
#             entity = Entity(
#                 item["guid"],
#                 item["name"],
#                 item["description"],
#                 item["mtype"],
#                 item["resources"],
#                 item["properties"],
#             )
#             self.entities.append(entity)

#     def save(self):
#         data = []
#         for entity in self.entities:
#             item = {
#                 "guid": entity.guid,
#                 "name": entity.name,
#                 "description": entity.description,
#                 "mtype": entity.mtype,
#                 "resources": entity.resources,
#                 "properties": entity.properties,
#             }
#             data.append(item)
#         save_data(self.filename, data)

#     def add(self, entity):
#         self.entities.append(entity)
#         self.save()

#     def update(self, entity):
#         for i, item in enumerate(self.entities):
#             if item.guid == entity.guid:
#                 self.entities[i] = entity
#                 self.save()
#                 break

#     def delete(self, entity):
#         for i, item in enumerate(self.entities):
#             if item.guid == entity.guid:
#                 del self.entities[i]
#                 self.save()
#                 break

#     def get(self, guid):
#         for entity in self.entities:
#             if entity.guid == guid:
#                 return entity
#         return None

#     def get_all(self):
#         return self.entities

#     def load_db(filename: str or Path) -> list:
#         fpath = Path(filename)
#         if fpath.exists():
#             with open(fpath, "r") as f:
#                 return json.load(f)
#         else:
#             return

#     @staticmethod
#     def save_db(filename, data) -> None:
#         fpath = Path(filename)
#         if fpath.exists():
#             print(f"{fpath} already exists, please use update_db()")
#         else:
#             with open(fpath, "w") as f:
#                 json.dump(data, f)
#         return

#     @staticmethod
#     def read_db(filename):
#         """Describe DB with Name, num_entities, entity types?"""
#         # Open file
#         # count entries
#         # get mtype set
#         ...

#     @staticmethod
#     def get_data(filename):
#         return load_db(filename)

#     @staticmethod
#     def save_data(filename, data):
#         save_db(filename, data)

#     @staticmethod
#     def add_data(filename, data):
#         data = get_data(filename)
#         data.append(data)
#         save_data(filename, data)

#     @staticmethod
#     def update_data(filename, data):
#         data = get_data(filename)
#         data.update(data)
#         save_data(filename, data)

#     @staticmethod
#     def delete_data(filename, data):
#         data = get_data(filename)
#         data.remove(data)
#         save_data(filename, data)


if __name__ == "__main__":
    root_path = Path("../tests/fixtures/metadata_databases/")
    fpath = root_path.joinpath("labs.json")
    bla = Entity()
    blaf = EntityFile(fpath)
    print(bla)
    print(blaf)
    print(0)
