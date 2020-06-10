import unittest
import common_py
import os
from typing import List, Callable


class TestListFilters(unittest.TestCase):
    def test_multiple_filters(self):
        filters: List[Callable[[str], bool]] = [
            lambda element: len(element) < 4,
            lambda element: element.startswith("a"),
        ]
        l: List[str] = common_py.list_filters(
            filters, ["Apply", "Board", "apply", "app", "acc", "block"]
        )
        self.assertEqual(len(l), 2)
        self.assertTrue(True if "app" in l else False)
        self.assertFalse(True if "apply" in l else False)
