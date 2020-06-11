import os
from pathlib import Path
from typing import List
import unittest

import common_py
from common_py.functional.either import Either


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


class TestRename(unittest.TestCase):
    base_folder = os.path.join("tests", "resources", "base")

    def setUp(self) -> None:
        create_common_base(self.base_folder)

    def tearDown(self) -> None:
        remove_common_base(self.base_folder)

    def test_rename_file(self):
        success: Either[str, Exception] = common_py.rename_file(
            "tiger.txt", "rabbit.txt", self.base_folder
        )
        result: str = os.path.join(self.base_folder, "rabbit.txt")
        self.assertEqual(success.right, result)
        self.assertTrue(os.path.exists(result))

    def test_rename_file_failure(self):
        failure: Either[str, Exception] = common_py.rename_file(
            "trax.txt", "rabbit.txt", self.base_folder
        )
        self.assertTrue(isinstance(failure.left, FileNotFoundError))
        result: str = os.path.join(self.base_folder, "rabbit.txt")
        self.assertFalse(os.path.exists(result))

    def test_rename_files(self):
        success: Either[List[str], Exception] = common_py.rename_files(
            [("tiger.txt", "rabbit.txt"), ("tile.txt", "fish.txt")], self.base_folder
        )
        files: List[str] = ["rabbit.txt", "fish.txt"]
        results: List[str] = list(
            map(lambda el: os.path.join(self.base_folder, el), files)
        )
        self.assertEqual(success.right, results)
        self.assertTrue(os.path.exists(results[0]))
        self.assertTrue(os.path.exists(results[1]))

    def test_rename_files_failure(self):
        failure: Either[List[str], Exception] = common_py.rename_files(
            [("tiger.txt", "rabbit.txt"), ("trax.txt", "fish.txt")], self.base_folder
        )
        self.assertTrue(isinstance(failure.left, FileNotFoundError))
        files: List[str] = ["rabbit.txt"]
        results: List[str] = list(
            map(lambda el: os.path.join(self.base_folder, el), files)
        )
        self.assertEqual(failure.right, results)
        self.assertTrue(os.path.exists(results[0]))
