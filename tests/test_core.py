#!/usr/bin/env python
# @File: tests/test_api.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Friday, January 13th 2023, 6:17:44 pm
import copy
import os
import tempfile
import json
import shutil
import unittest
import uuid
from datetime import datetime
from genemede.core import EntityFile, Entity
from pathlib import Path


class TestEntity(unittest.TestCase):
    def test_init_with_no_arg(self):
        e = Entity()
        self.assertIsNotNone(e.guid)  # type: ignore
        self.assertIsNotNone(e.datetime)  # type: ignore
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


class TestEntityFile(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"name": "test1", "description": "Test Entity 1"},
            {"name": "test2", "description": "Test Entity 2"},
            {"name": "test3", "description": "Test Entity 3"},
        ]
        self.test_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_path = self.test_file.name
        with open(self.test_path, "w") as f:
            json.dump(self.test_data, f, indent=4)
        # Create valid file with correct entity keys inside
        self.valid_data = [dict.fromkeys(Entity.template), dict.fromkeys(Entity.template)]
        self.valid_file = tempfile.NamedTemporaryFile(delete=False)
        self.valid_path = self.valid_file.name
        with open(self.valid_path, "w") as f:
            json.dump(self.valid_data, f, indent=4)

    def tearDown(self):
        os.remove(self.test_path)

    def test_read(self):
        data = EntityFile.read(self.test_path)
        self.assertEqual(data, self.test_data)

    def test_write(self):
        new_data = [
            {"name": "test4", "description": "Test Entity 4"},
            {"name": "test5", "description": "Test Entity 5"},
        ]
        EntityFile.write(self.test_path, new_data)
        with open(self.test_path, "r") as f:
            written_data = json.load(f)
        self.assertEqual(written_data, new_data)

    def test_backup(self):
        EntityFile.backup(self.test_path)
        # Find the EntityFile just created with the backup mathod
        backup_path = next(Path(self.test_path).parent.glob("*_bak_*"))
        self.assertTrue(os.path.exists(backup_path))
        os.remove(backup_path)

    def test_validate_file(self):
        """test_path file is invalid since creation its keys do not match the
        template of the Entity object"""
        # Test that it's not valid
        with self.assertRaises(AssertionError):
            EntityFile.validate_file(self.test_path)
        # Create a valid file to test and test it
        valid_path = Path(self.test_path).with_name("valid_test.json")
        valid_data = [dict.fromkeys(Entity.template)]
        EntityFile.write(valid_path, valid_data)

        self.assertTrue(EntityFile.validate_file(valid_path))
        valid_path.unlink()

    def test_load(self):
        with self.assertRaises(AssertionError):
            EntityFile(self.test_path)
        # Create a valid file to test and test it
        valid_path = Path(self.test_path).with_name("valid_test.json")
        valid_data = [dict.fromkeys(Entity.template)]
        EntityFile.write(valid_path, valid_data)
        self.assertTrue(EntityFile(valid_path))
        valid_path.unlink()

    def test_check_guids(self):
        # Test with valid guids
        entities = [Entity(item=d) for d in self.valid_data]
        entity_file = EntityFile(self.valid_path)
        entity_file.ents = entities
        # Test with valid uuids
        entities[0].guid = str(uuid.uuid4())
        entities[1].guid = str(uuid.uuid4())

        self.assertTrue(entity_file.check_guids())

        # Test with missing or invalid guids
        entities[0].guid = None
        self.assertFalse(entity_file.check_guids())
        entities[0].guid = 1234
        self.assertFalse(entity_file.check_guids())

    def test_fix_guids(self):
        # Test with dry_run=True
        entities = [Entity(item=d) for d in self.valid_data]
        entities[0].guid = "asdasd"
        entity_file = EntityFile(self.valid_path)
        entity_file.ents = copy.deepcopy(entities)
        entity_file.fix_guids(dry_run=True)
        self.assertTrue(entity_file.ents == entities)
        # Test with dry_run=False
        entity_file.fix_guids(dry_run=False)
        self.assertFalse(entity_file.ents == entities)


if __name__ == "__main__":
    unittest.main()
