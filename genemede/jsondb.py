#!/usr/bin/env python
# @File: nico/jsondb.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:44:55 pm
import json
from pathlib import Path


def load_db(filename: str or Path) -> list:
    fpath = Path(filename)
    if fpath.exists():
        with open(fpath, "r") as f:
            return json.load(f)
    else:
        return


def save_db(filename, data) -> None:
    fpath = Path(filename)
    if fpath.exists():
        print(f"{fpath} already exists, please use update_db()")
    else:
        with open(fpath, "w") as f:
            json.dump(data, f)
    return


def read_db(filename):
    """Describe DB with Name, num_entities, entity types?"""
    # Open file
    # count entries
    # get mtype set
    ...

def get_data(filename):
    return load_json(filename)


def save_data(filename, data):
    save_json(filename, data)


def add_data(filename, data):
    data = get_data(filename)
    data.append(data)
    save_data(filename, data)


def update_data(filename, data):
    data = get_data(filename)
    data.update(data)
    save_data(filename, data)


def delete_data(filename, data):
    data = get_data(filename)
    data.remove(data)
    save_data(filename, data)


"""
1. Define the footprint of an entry into the database called Entity containing: guid, name, description, mtype, resources, and properties as fields.
"""


class Entity:
    def __init__(self, guid, name, description, mtype, resources, properties):
        self.guid = guid
        self.name = name
        self.description = description
        self.mtype = mtype
        self.resources = resources
        self.properties = properties


"""
3. Create a class called EntityDB that contains a list of Entity objects.
"""


class EntityDB:
    def __init__(self, filename):
        self.filename = filename
        self.entities = []
        self.load()

    def load(self):
        data = get_data(self.filename)
        for item in data:
            entity = Entity(
                item["guid"],
                item["name"],
                item["description"],
                item["mtype"],
                item["resources"],
                item["properties"],
            )
            self.entities.append(entity)

    def save(self):
        data = []
        for entity in self.entities:
            item = {
                "guid": entity.guid,
                "name": entity.name,
                "description": entity.description,
                "mtype": entity.mtype,
                "resources": entity.resources,
                "properties": entity.properties,
            }
            data.append(item)
        save_data(self.filename, data)

    def add(self, entity):
        self.entities.append(entity)
        self.save()

    def update(self, entity):
        for i, item in enumerate(self.entities):
            if item.guid == entity.guid:
                self.entities[i] = entity
                self.save()
                break

    def delete(self, entity):
        for i, item in enumerate(self.entities):
            if item.guid == entity.guid:
                del self.entities[i]
                self.save()
                break

    def get(self, guid):
        for entity in self.entities:
            if entity.guid == guid:
                return entity
        return None

    def get_all(self):
        return self.entities


"""
4. Create the same interface in functional form
"""


def get_data(filename):
    return load_json(filename)


def save_data(filename, data):
    save_json(filename, data)


def add_data(filename, data):
    data = get_data(filename)
    data.append(data)
    save_data(filename, data)


def update_data(filename, data):
    data = get_data(filename)
    data.update(data)
    save_data(filename, data)


def delete_data(filename, data):
    data = get_data(filename)
    data.remove(data)
    save_data(filename, data)


def get_entity(filename, guid):
    data = get_data(filename)
    for item in data:
        if item["guid"] == guid:
            return item
    return None


def get_all_entities(filename):
    return get_data(filename)


def add_entity(filename, entity):
    data = get_data(filename)
    data.append(entity)
    save_data(filename, data)


def update_entity(filename, entity):
    data = get_data(filename)
    for i, item in enumerate(data):
        if item["guid"] == entity["guid"]:
            data[i] = entity
            save_data(filename, data)
            break


def delete_entity(filename, entity):
    data = get_data(filename)
    for i, item in enumerate(data):
        if item["guid"] == entity["guid"]:
            del data[i]
            save_data(filename, data)
            break


"""
Define the footprint of an entry into the database called entity containing: guid, name, description, mtype, resources, and properties as fields. Use json format
"""

import json


class Entity:
    def __init__(self, guid, name, description, mtype, resources, properties):
        self.guid = guid
        self.name = name
        self.description = description
        self.mtype = mtype
        self.resources = resources
        self.properties = properties

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


"""
Create a class called EntityDatabase that contains a list of entities.
"""


class EntityDatabase:
    def __init__(self, entities):
        self.entities = entities

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


"""
Create a class called EntityManager that contains a list of EntityDatabase objects.
"""


class EntityManager:
    def __init__(self, entity_databases):
        self.entity_databases = entity_databases

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)



if __name__ == "__main__":
    fname = '/home/nico/Projects/COGITATE/GENEMEDE/genemede/scratch-test.json'
