import unittest
import common_py
import os
from typing import List
from pathlib import Path


class TestFilesInFolder(unittest.TestCase):
    resource_folder: str = os.path.join("tests", "resources")

    def test_all_files(self):
        files: List[str] = common_py.files_in_folder(
            self.resource_folder, include_hidden_file=True
        )
        self.assertEqual(len(files), 4)

    def test_files_without_hidden_file(self):
        files: List[str] = common_py.files_in_folder(
            self.resource_folder, include_hidden_file=False
        )
        self.assertEqual(len(files), 3)


class TestCreateFolderIfNotExist(unittest.TestCase):
    def test_create(self):
        folder_name = os.path.join("tests", "resources", "a")
        common_py.create_folder_if_not_exist(folder_name)
        self.assertTrue(os.path.exists(folder_name))

        Path(folder_name).rmdir()
