#!/usr/bin/env python
# @File: tests/test_api.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, January 13th 2023, 6:17:44 pm
import unittest
from genemede.api import Entity


class TestEntity(unittest.TestCase):
    def test_init_with_no_arg(self):
        e = Entity()
        self.assertIsNone(e.guid)
        self.assertIsNone(e.datetime)
        self.assertIsNone(e.name)
        self.assertIsNone(e.description)
        self.assertIsNone(e.mtype)
        self.assertIsNone(e.resources)
        self.assertIsNone(e.properties)
        self.assertIsNone(e.custom)
        self.assertIsNone(e.bids)

    def test_init_with_valid_dict(self):
        item = {
            "guid": "123",
            "datetime": "2022-01-01",
            "name": "test",
            "description": "test description",
            "mtype": "test type",
            "resources": [],
            "properties": [],
            "custom": [],
            "bids": [],
        }
        e = Entity(item)
        self.assertEqual(e.guid, "123")
        self.assertEqual(e.datetime, "2022-01-01")
        self.assertEqual(e.name, "test")
        self.assertEqual(e.description, "test description")
        self.assertEqual(e.mtype, "test type")
        self.assertEqual(e.resources, [])
        self.assertEqual(e.properties, [])
        self.assertEqual(e.custom, [])
        self.assertEqual(e.bids, [])

    def test_init_with_invalid_dict(self):
        item = {"invalid_key": "invalid_value"}
        with self.assertRaises(KeyError):
            e = Entity(item)

    def test_init_with_non_dict(self):
        item = "not a dict"
        with self.assertRaises(TypeError):
            e = Entity(item)


if __name__ == "__main__":
    unittest.main()
