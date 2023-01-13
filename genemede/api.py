#!/usr/bin/env python
# @File: nico/jsondb.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:44:55 pm
import json
from pathlib import Path


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
        print(self.__dict__)

    def from_dict(self, item):
        if not isinstance(item, dict):
            raise TypeError(f"{item} <- not a dict")
        if any([k not in self.template for k in item.keys()]):
            raise KeyError(f"{item} <- does not match template")

        for k, v in item.items():
            self.__dict__.update({k: v})


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
    fname = "../tests/fixtures/metadata_databases/"
    bla = Entity()
    print(0)
