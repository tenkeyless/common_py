import os
from pathlib import Path
from typing import List
import unittest

import common_py
from common_py.functional.either import Either, Right


def create_common_base(base_folder: str) -> None:
    Path(base_folder).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(base_folder, "tiger.txt"), "w") as file:
        file.write("tiger")
    with open(os.path.join(base_folder, ".hidden.txt"), "w") as file:
        file.write("hidden")
    with open(os.path.join(base_folder, "tile.txt"), "w") as file:
        file.write("tile")
    with open(os.path.join(base_folder, "robot.txt"), "w") as file:
        file.write("robot")


def remove_common_base(base_folder: str) -> None:
    for file in os.listdir(base_folder):
        os.remove(os.path.join(base_folder, file))
    Path(base_folder).rmdir()


class TestFilesInFolder(unittest.TestCase):
    base_folder = os.path.join("tests", "resources", "base")

    def setUp(self) -> None:
        create_common_base(self.base_folder)

    def tearDown(self) -> None:
        remove_common_base(self.base_folder)

    def test_all_files(self):
        # [success] get files in folder.
        files: List[str] = common_py.files_in_folder(
            self.base_folder, include_hidden_file=True
        )
        self.assertEqual(len(files), 4)

    def test_files_without_hidden_file(self):
        # [success] get files in folder without hidden files.
        files: List[str] = common_py.files_in_folder(
            self.base_folder, include_hidden_file=False
        )
        self.assertEqual(len(files), 3)


class TestCreateFolder(unittest.TestCase):
    folder_name = os.path.join("tests", "resources", "create")

    def tearDown(self):
        Path(self.folder_name).rmdir()
        self.assertFalse(os.path.exists(self.folder_name))

    def test_create_folder_success(self):
        # [success] create folder.
        success: Either[str, Exception] = common_py.create_folder(self.folder_name)
        self.assertEqual(success.right, self.folder_name)
        self.assertTrue(os.path.exists(self.folder_name))

    def test_create_folder_error_if_exist(self):
        # pre processing - create folder.
        success: Either[str, Exception] = common_py.create_folder(self.folder_name)
        self.assertEqual(success.right, self.folder_name)
        self.assertTrue(os.path.exists(self.folder_name))

        # [failure] create folder if exist.
        left: Either[str, Exception] = common_py.create_folder(
            self.folder_name, exist_ok=False
        )

        self.assertTrue(isinstance(left.left, FileExistsError))
        self.assertTrue(os.path.exists(self.folder_name))


class TestCopyAllFile(unittest.TestCase):
    base_folder = os.path.join("tests", "resources", "base")
    target_folder = os.path.join("tests", "resources", "copied")

    def setUp(self) -> None:
        create_common_base(self.base_folder)
        success_create_folder: Either[str, Exception] = common_py.create_folder(
            self.target_folder
        )
        self.assertEqual(success_create_folder.right, self.target_folder)
        self.assertTrue(os.path.exists(self.target_folder))

    def tearDown(self) -> None:
        remove_common_base(self.base_folder)
        remove_common_base(self.target_folder)

    def test_copy_all_file(self):
        # [success] copy all file.
        success: Either[int, Exception] = common_py.copy_all_file(
            self.base_folder, self.target_folder
        )
        self.assertEqual(success.right, 4)
        self.assertTrue(os.path.exists(self.target_folder))


class TestMoveAllFile(unittest.TestCase):
    base_folder = os.path.join("tests", "resources", "base")
    target_folder = os.path.join("tests", "resources", "moved")

    def setUp(self) -> None:
        create_common_base(self.base_folder)
        success_create_folder: Either[str, Exception] = common_py.create_folder(
            self.target_folder
        )
        self.assertEqual(success_create_folder.right, self.target_folder)
        self.assertTrue(os.path.exists(self.target_folder))

    def tearDown(self) -> None:
        remove_common_base(self.base_folder)
        remove_common_base(self.target_folder)

    def test_move_all_file(self):
        success: Either[int, Exception] = common_py.move_all_file(
            self.base_folder, self.target_folder
        )
        self.assertEqual(success.right, 4)
        self.assertTrue(os.path.exists(self.target_folder))
