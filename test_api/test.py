#!/usr/bin/env python
# @File: nico/test.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 1:06:21 pm
"""
Define a representation using json files of the contents of an image that contains the sketch of an experimental setup's wiring diagram. Add the user as one of the nodes.
"""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt

import itertools
import json
import networkx as nx

# import cv2

def save_json_file(filename, dat):
    """
    Save json file
    """

    json.dump(dat, open(filename, "w"), indent=2, sort_keys=True)
    print("JSON file saved: {}".format(filename))


def load_json_file(filepath):
    """
    Load json file
    """
    if os.path.isfile(filepath):
        return json.load(open(filepath, "r"))
    else:
        print("File not found:\n\t{}".format(filepath))
        return {}


class Node(object):
    """
    The nodes of the graph formed by the experimental setup.
    """

    def __init__(self, name, attr):
        """
        Initialisation
        """

        super(Node, self).__init__()

        self.name = name
        self.attr = attr
        self.rels = []

    def __repr__(self):
        """
        Print the name
        """

        return self.name

    def add_relation(self, rel):
        """
        Set the name of the node
        """

        self.rels.append(rel)

    def visualize_relations(self):
        """
        Visualize the relations
        """

        print("\n{}".format(self.name))
        print("\t{}".format(", ".join(self.rels)))


class Relation(object):
    """
    The set of relations between the nodes in the graph.
    """

    def __init__(self, name, attr):
        """
        Initialisation
        """

        super(Relation, self).__init__()

        self.name = name
        self.attr = attr

    def __repr__(self):
        """
        Print the name
        """

        return self.name


class ExperimentalSetup(object):
    """
    The graph formed by the experimental setup using custom nodes and set of relations for this type of experiment.
    """

    def __init__(self, name, attr):
        """
        Initialisation
        """

        super(ExperimentalSetup, self).__init__()

        self.name = name
        self.attr = attr

        self.graph = nx.Graph()
        self.nodes = {}
        self.relations = {}

    def __repr__(self):
        """
        Print the name
        """

        return self.name

    def add_relation(self, node1, node2, relation):
        """
        Add relation between two det.
        """

        self.graph.add_edge(node1, node2, relation=relation)
        node1.add_relation(relation)
        node2.add_relation(relation)

    def visualize_graph(self, save_name=None, figsize=(18, 12)):
        """
        Visualize the graph formed by the experimental setup.
        """

        plt.figure(figsize=figsize)
        pos = nx.circular_layout(self.graph)
        nx.draw(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.axis("off")

        if save_name is not None:
            plt.savefig(save_name, bbox_inches="tight")

    def visualize_nodes(self):
        """
        Visualize the nodes and their connections in the graph.
        """

        for key, val in self.nodes.iteritems():
            val.visualize_relations()


class JSON2Graph(object):
    """
    Transforming the nodes and relations information stored in a json file to its corresponding graph representation.
    """

    def __init__(self, json_file):
        """
        Initialisation
        """

        super(JSON2Graph, self).__init__()

        self.json_file = json_file

        if os.path.isfile(self.json_file):
            dat = json.load(open(self.json_file, "r"))
            self.name = dat["name"]
            self.attr = dat["attr"]

            self.graph = nx.Graph()
            self.nodes = {}
            self.relations = {}

            self.create_all_nodes()
            self.create_all_relations()
            self.create_graph()
        else:
            print("File not found:\n\t{}".format(self.json_file))

    def __repr__(self):
        """
        Print the name
        """

        return self.name

    def create_all_nodes(self):
        """
        Create all the user deined experimental setup nodes from the json file
        """

        for det in self.attr["nodes"]:
            self.nodes[det["name"]] = Node(det, self.attr["nodes"][det["name"]])

    def create_all_relations(self):
        """
        Create all the user defined experimental setup relations.
        """

        if "relations" in self.attr.keys():
            for det in self.attr["relations"]:
                self.relations[det] = Relation(det, self.attr["relations"][det])

    def create_graph(self):
        """
        Create the graph formed by the experimental setup based on its deifned nodes and set of relations.
        """

        # Iterate through the relations
        for rel in self.attr["relations"]:
            # Iterate through the nodes in a relation
            for key in self.attr["relations"][rel]:
                # Get the nodes that have the relation
                nodes = self.attr["relations"][rel][key]
                # Generate combinations of existing nodes
                for comb in itertools.combinations(nodes, 2):
                    # Add the relation between the node pair
                    self.graph.add_edge(self.nodes[comb[0]], self.nodes[comb[1]], relation=rel)

                    # Add the relation to each node's relations list
                    self.nodes[comb[0]].add_relation(rel)
                    self.nodes[comb[1]].add_relation(rel)

    def create_node(self, name, attr, color=(0, 0, 255), vertexsize=5):
        """
        Create an annotated node using the information provided.
        """

        self.graph.add_node(name)

        text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        text_top = attr[1] - 10
        text_pos = (attr[0] - text_size[0] / 2, text_top)
        cv2.putText(self.image, name, text_pos, cv2.FONT_HERSHEY_PLAIN, 1, color, 1)
        pos = (attr[0], attr[1])
        cv2.circle(self.image, pos, vertexsize, color, -1)

    def create_edge(self, node1, node2, name, color=(0, 255, 0), radius=5):
        """
        Create an annotated edge using the information provided.
        """

        cv2.line(self.image, node1, node2, color)
        text_size = cv2.getTextSize(name, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
        text_top = (node1[1] + node2[1]) / 2 - 10
        text_pos = (node1[0] - text_size[0] / 2, text_top)
        cv2.putText(self.image, name, text_pos, cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

        # middle_point = ((node1[0] + node2[0])/2, (node1[1]+node2[1])/2)
        # cv2.circle(self.image, middle_point, radius, color, -1)

    def visualize_nodes(self, save_name="annotated_nodes.png", color=(0, 0, 255), vertexsize=5):
        """
        Visualize the nodes and their connections in the graph.
        """

        for nd in self.graph.nodes:
            self.create_node(nd.name, nd.attr["pos"], color=color, vertexsize=vertexsize)

        cv2.imwrite(save_name, self.image)

    def visualize_relations(
        self, save_name="annotated_relations.png", color=(0, 255, 0), radius=5
    ):
        """
        Visualize the nodes and their connections in the graph.
        """

        for edge in self.graph.edges:
            # print edge[0].name
            # print edge[1].name
            # print self.graph[edge[0]][edge[1]]['relation']
            # print '\n'
            self.create_edge(
                edge[0].attr["pos"],
                edge[1].attr["pos"],
                self.graph[edge[0]][edge[1]]["relation"],
                color=color,
                radius=radius,
            )

        cv2.imwrite(save_name, self.image)

    def visualize_graph(self, save_name=None, figsize=(18, 12)):
        """
        Visualize the graph formed by the experimental setup.
        """

        plt.figure(figsize=figsize)
        pos = nx.circular_layout(self.graph)
        nx.draw(self.graph, pos)
        nx.draw_networkx_labels(self.graph, pos)
        plt.axis("off")

        if save_name is not None:
            plt.savefig(save_name, bbox_inches="tight")


def main():
    """
    Main function
    """

    # Image file to load
    image_file = "wiring_schematic.png"
    # Json file to store the information
    # json_file = "wiring_schematic.json"
    json_file = "../protoeln/exp1/meg/BU/setup.json"

    # If a json file containing the nodes and relations is provided, convert it to its graph representation
    if os.path.isfile(json_file):
        json2graph = JSON2Graph(json_file)
        # json2graph.visualize_graph(save_name='graph.png')
        json2graph.visualize_nodes(save_name="annotated_nodes.png")
        json2graph.visualize_relations(save_name="annotated_relations.png")


if __name__ == "__main__":
    main()
