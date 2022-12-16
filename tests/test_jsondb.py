#!/usr/bin/env python
# @File: nico/test_jsondb.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, July 15th 2022, 12:47:08 pm

import unittest
from genemede.jsondb import *
from pathlib import Path

sorted()


class TestJsonDatabase(unittest.TestCase):
    def setUp(self):
        print("\n" * 5, Path().cwd(), "\n" * 5)
        self.filename = "./fixtures/temp/scratch-test.json"
        self.projects = "./fixtures/metadata_databases/projects.json"
        self.data = {"test": "test"}

    def test_load_json(self):
        self.assertEqual(load_json(self.projects))

    def test_save_json(self):
        save_json(self.filename, self.data)
        self.assertEqual(load_json(self.filename), self.data)

    def test_get_data(self):
        self.assertEqual(get_data(self.filename), self.data)

    def test_save_data(self):
        save_data(self.filename, self.data)
        self.assertEqual(get_data(self.filename), self.data)

    def test_add_data(self):
        add_data(self.filename, self.data)
        self.assertEqual(get_data(self.filename), self.data)

    def test_update_data(self):
        update_data(self.filename, self.data)
        self.assertEqual(get_data(self.filename), self.data)

    def test_delete_data(self):
        delete_data(self.filename, self.data)
        self.assertEqual(get_data(self.filename), self.data)


if __name__ == "__main__":
    unittest.main()
