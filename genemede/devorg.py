#!/usr/bin/env python
# @File: protoeln/nodes.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Thursday, July 7th 2022, 2:50:58 pm
"""Python interface for defining, adding, removing, reading, and writing nodes to the nodes.json file."""
# Implement the API for the nodes.json file.
# The nodes.json file is a JSON file that contains a list of nodes.
# The nodes.json file is used to store the nodes that are added to a graph that represents a setup.
import json
import uuid
from dataclasses import dataclass

from pysondb import db

data = db.getDb("testdb.json")

class Entity:
    """A generic entity."""

    def __init__(self, name, type, guid=None, description="", resources={}, properties={}):
        """Initialize the entity."""
        if guid is None:
            id = str(uuid.uuid4())
        self.guid = id
        self.name = name
        self.description = description
        self.type = type
        self.resources = resources
        self.properties = properties

    def __str__(self):
        """Return the string representation of the entity."""
        return json.dumps(self.to_dict())

    def to_dict(self):
        """Return the dictionary representation of the entity."""
        return {
            "guid": self.guid,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "resources": self.resources,
            "properties": self.properties,
        }

    def to_json(self):
        """Return the json representation of the entity."""
        return json.dumps(self.to_dict())

    def from_json(self, json_str):
        """Load the entity from a json string."""
        self.__dict__ = json.loads(json_str)

    def from_dict(self, dict):
        """Load the entity from a dictionary."""
        self.__dict__ = dict

    def __repr__(self):
        """Return the representation of the entity."""
        return str(self)

    def __eq__(self, other):
        """Return True if the entities are equal."""
        return self.guid == other.guid

    def __ne__(self, other):
        """Return True if the entities are not equal."""
        return self.guid != other.guid

    def __hash__(self):
        """Return the hash of the entity."""
        return hash(self.guid)

    def _validate_type

class Node(Entity):
    """A node."""

    def __init__(self, name, type, guid=None, description="", resources={}, properties={}):
        """Initialize the node."""
        super().__init__(name, type, guid, description, resources, properties)


def load_types(template_file="type_templates.json"):
    """Load the types."""
    with open(template_file, "r") as f:
        types = json.load(f)
    return [x for x in types]



def validate_setup_db(fpath='devices.json'):
    """Validate the setup."""
    nodes = get_nodes()
    node_names = [node["name"] for node in nodes]
    for node in node_list:
        if node not in node_names:
            return False
    return True


def validate_setup_edges(edge_list):
    """Validate the setup."""
    edges = get_edges()
    edge_names = [edge["name"] for edge in edges]
    for edge in edge_list:
        if edge not in edge_names:
            return False
    return True


def get_nodes():
    """Return the list of nodes."""
    with open("nodes.json", "r") as f:
        nodes = json.load(f)
    return nodes


def add_node(node):
    """Add a node to the nodes.json file."""
    nodes = get_nodes()
    nodes.append(node)
    with open("nodes.json", "w") as f:
        json.dump(nodes, f, indent=4)


def remove_node(node):
    """Remove a node from the nodes.json file."""
    nodes = get_nodes()
    nodes.remove(node)
    with open("nodes.json", "w") as f:
        json.dump(nodes, f, indent=4)


def get_node(node_name):
    """Return the node with the given name."""
    nodes = get_nodes()
    for node in nodes:
        if node["name"] == node_name:
            return node
    return None


def get_node_by_id(node_id):
    """Return the node with the given id."""
    nodes = get_nodes()
    for node in nodes:
        if node["id"] == node_id:
            return node
    return None


def get_node_by_type(node_type):
    """Return the node with the given type."""
    nodes = get_nodes()
    for node in nodes:
        if node["type"] == node_type:
            return node
    return None


def get_node_by_name(node_name):
    """Return the node with the given name."""
    nodes = get_nodes()
    for node in nodes:
        if node["name"] == node_name:
            return node
    return None


class Node:
    """A class that represents a node."""

    def __init__(self, name, description=None, type=None, resources=None, properties=None):
        """Initialize the node."""
        self.guid = uuid.uuid4()
        self.name = name
        self.description = description
        self.type = type
        self.resources = resources
        self.properties = properties

    def __str__(self):
        """Return a string representation of the node."""
        return self.name

    def __repr__(self):
        """Return a string representation of the node."""
        return self.name

    def __eq__(self, other):
        """Return True if the nodes are equal."""
        return self.name == other.name and self.type == other.type

    def __hash__(self):
        """Return the hash of the node."""
        return hash(self.name)

    def to_json(self):
        """Return the node as a JSON object."""
        return {
            "id": self.guid,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "resources": self.resources,
            "properties": self.properties,
        }

    @staticmethod
    def from_json(json_obj):
        """Return the node from a JSON object."""
        return Node(
            json_obj["name"],
            json_obj["description"],
            json_obj["type"],
            json_obj["resources"],
            json_obj["properties"],
        )

    @staticmethod
    def from_dict(dict_obj):
        """Return the node from a dictionary object."""
        return Node(
            dict_obj["name"],
            dict_obj["description"],
            dict_obj["type"],
            dict_obj["resources"],
            dict_obj["properties"],
        )

    @staticmethod
    def from_json_file(json_file):
        """Return the node from a JSON file."""
        with open(json_file, "r") as f:
            json_obj = json.load(f)
        return Node.from_json(json_obj)

    @staticmethod
    def from_dict_file(dict_file):
        """Return the node from a dictionary file."""
        with open(dict_file, "r") as f:
            dict_obj = json.load(f)
        return Node.from_dict(dict_obj)

    def to_json_file(self, json_file):
        """Write the node to a JSON file."""
        with open(json_file, "w") as f:
            json.dump(self.to_json(), f, indent=4)

    def to_dict_file(self, dict_file):
        """Write the node to a dictionary file."""
        with open(dict_file, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        """Return the node as a dictionary object."""
        return {
            "id": self.guid,
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "resources": self.resources,
            "properties": self.properties,
        }


# Implement a class that represents the nodes.json file.
# The nodes.json file is a JSON file that contains a list of nodes.
# The nodes.json file is used to store the nodes that are added to a graph that represents a setup.
class Nodes:
    """A class that represents the nodes.json file."""

    def __init__(self):
        """Initialize the nodes.json file."""
        self.nodes = []

    def __str__(self):
        """Return a string representation of the nodes.json file."""
        return str(self.nodes)

    def __repr__(self):
        """Return a string representation of the nodes.json file."""
        return str(self.nodes)

    def __eq__(self, other):
        """Return True if the nodes.json files are equal."""
        return self.nodes == other.nodes

    def __hash__(self):
        """Return the hash of the nodes.json file."""
        return hash(self.nodes)

    def to_json(self):
        """Return the nodes.json file as a JSON object."""
        return self.nodes

    @staticmethod
    def from_json(json_obj):
        """Return the nodes.json file from a JSON object."""
        nodes = Nodes()
        nodes.nodes = json_obj
        return nodes

    @staticmethod
    def from_json_file(json_file):
        """Return the nodes.json file from a JSON file."""
        with open(json_file, "r") as f:
            json_obj = json.load(f)
        return Nodes.from_json(json_obj)

    def to_json_file(self, json_file):
        """Write the nodes.json file to a JSON file."""
        with open(json_file, "w") as f:
            json.dump(self.to_json(), f, indent=4)

    def to_dict(self):
        """Return the nodes.json file as a dictionary object."""
        return self.nodes

    def to_dict_file(self, dict_file):
        """Write the nodes.json file to a dictionary file."""
        with open(dict_file, "w") as f:
            json.dump(self.to_dict(), f, indent=4)


if __name__ == "__main__":
    # Test the Node class.
    node = Node(
        "node1",
        "node1 description",
        "node1 type",
        {"resource1": "resource1 value"},
        {"property1": "property1 value"},
    )
    print(node)
    print(node.to_json())
    print(node.to_dict())
    print(Node.from_json(node.to_json()))
    print(Node.from_dict(node.to_dict()))
    print(Node.from_json_file("node1.json"))
    print(Node.from_dict_file("node1.json"))
    node.to_json_file("node1.json")
    node.to_dict_file("node1.json")
    print(Node.from_json_file("node1.json"))
    print(Node.from_dict_file("node1.json"))
    # Test the Nodes class.
    nodes = Nodes()
    nodes.nodes.append(node)
    print(nodes)
    print(nodes.to_json())
    print(nodes.to_dict())
    print(Nodes.from_json(nodes.to_json()))
    print(Nodes.from_dict(nodes.to_dict()))
    print(Nodes.from_json_file("nodes.json"))
    print(Nodes.from_dict_file("nodes.json"))
    nodes.to_json_file("nodes.json")
    nodes.to_dict_file("nodes.json")
    print(Nodes.from_json_file("nodes.json"))
    print(Nodes.from_dict_file("nodes.json"))
    # Test the get_node_by_name() function.
    print(get_node_by_name("node1"))
    print(get_node_by_name("node2"))
    # Test the get_node_by_id() function.
    print(get_node_by_id(node.guid))
    print(get_node_by_id("node2"))
