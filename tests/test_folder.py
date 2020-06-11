import os
from pathlib import Path
from typing import List
import unittest

import common_py
from common_py.functional.either import Either, Right


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


class TestCreateFolder(unittest.TestCase):
    def test_create_folder_success(self):
        # [success] create folder
        folder_name = os.path.join("tests", "resources", "a")
        success: Either[str, Exception] = common_py.create_folder(folder_name)
        self.assertEqual(success.right, folder_name)
        self.assertTrue(os.path.exists(folder_name))

        # post processing - delete folder
        Path(folder_name).rmdir()
        self.assertFalse(os.path.exists(folder_name))

    def test_create_folder_error_if_exist(self):
        # [success] create folder
        folder_name = os.path.join("tests", "resources", "a")
        success: Either[str, Exception] = common_py.create_folder(folder_name)
        self.assertEqual(success.right, folder_name)
        self.assertTrue(os.path.exists(folder_name))

        # [failure] create folder if exist
        left: Either[str, Exception] = common_py.create_folder(
            folder_name, exist_ok=False
        )
        self.assertEqual(left.left, FileExistsError)
        self.assertTrue(os.path.exists(folder_name))

        # post processing - delete folder
        Path(folder_name).rmdir()
        self.assertFalse(os.path.exists(folder_name))
