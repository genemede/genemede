#!/usr/bin/env python
# @File: tests/test_io.py
# @Author: Niccolo' Bonacchi (@nbonacchi)
# @Date: Tuesday, April 18th 2023, 10:29:52 am

import json
import tempfile
import unittest
from pathlib import Path
from genemede.io import create, read, update, backup


# Implement tests for genemede.io functions
class TestIO(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_data = [
            {
                "guid": "test_guid",
                "datetime": "test_datetime",
                "name": "test_name",
                "description": "test_description",
                "mtype": "test_mtype",
                "resources": [
                    {"guid": "test_guid", "datetime": "test_datetime", "name": "test_name"}
                ],
                "properties": [
                    {"guid": "test_guid", "datetime": "test_datetime", "name": "test_name"}
                ],
                "custom": [
                    {"guid": "test_guid", "datetime": "test_datetime", "name": "test_name"}
                ],
                "bids": [{"guid": "test_guid", "datetime": "test_datetime", "name": "test_name"}],
            },
        ]

    def test_create(self):
        create(self.temp_dir / "test_file.gnmd", self.test_data)
        self.assertTrue(self.temp_dir.joinpath("test_file.gnmd").exists())
        self.assertTrue(self.temp_dir.joinpath("test_file.gnmd").is_file())

    def test_read(self):
        create(self.temp_dir / "test_file.gnmd", self.test_data)
        e = read(self.temp_dir / "test_file.gnmd")
        self.assertIsNotNone(e)
        self.assertEqual(len(e), len(self.test_data))
        self.assertEqual(e[0]["guid"], self.test_data[0]["guid"])
        self.assertEqual(e[0] == self.test_data[0], True)

    def test_backup(self):
        # Create file
        create(self.temp_dir / "test_file.gnmd", self.test_data)
        # Backup created file
        backup(self.temp_dir / "test_file.gnmd")
        # List all files in temp_dir
        files = self.temp_dir.glob("*.gnmd")
        self.assertTrue(len([x for x in files if "test_file" in x.name]) >= 2)
