#!/usr/bin/env python
# @File: tests/test_api.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, January 13th 2023, 6:17:44 pm
import unittest
from genemede.api import Entity


class TestEntity(unittest.TestCase):
    def test_init_with_no_arg(self):
        e = Entity()
        self.assertIsNone(e.guid)  # type: ignore
        self.assertIsNone(e.datetime)  # type: ignore
        self.assertIsNone(e.name)  # type: ignore
        self.assertIsNone(e.description)  # type: ignore
        self.assertIsNone(e.mtype)  # type: ignore
        self.assertIsNone(e.resources)  # type: ignore
        self.assertIsNone(e.properties)  # type: ignore
        self.assertIsNone(e.custom)  # type: ignore
        self.assertIsNone(e.bids)  # type: ignore

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
        self.assertEqual(e.guid, "123")  # type: ignore
        self.assertEqual(e.datetime, "2022-01-01")  # type: ignore
        self.assertEqual(e.name, "test")  # type: ignore
        self.assertEqual(e.description, "test description")  # type: ignore
        self.assertEqual(e.mtype, "test type")  # type: ignore
        self.assertEqual(e.resources, [])  # type: ignore
        self.assertEqual(e.properties, [])  # type: ignore
        self.assertEqual(e.custom, [])  # type: ignore
        self.assertEqual(e.bids, [])  # type: ignore

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
