from typing import Callable, List
import unittest

import common_py


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


class TestCompareHashableList(unittest.TestCase):
    def test_compare_hashable_list_success(self):
        l1: List[str] = ["orange", "car"]
        l2: List[str] = ["lemon", "apple"]
        l3: List[int] = [2, 3, 5]
        self.assertTrue(common_py.compare_hashable_list(l1, l1))
        self.assertFalse(common_py.compare_hashable_list(l1, l2))
        self.assertFalse(common_py.compare_hashable_list(l1, l3))


class TestCompareOrderableList(unittest.TestCase):
    def test_compare_orderable_list_success(self):
        l1: List[str] = ["orange", "car"]
        l2: List[str] = ["lemon", "apple"]
        l3: List[int] = [2, 3, 5]
        self.assertTrue(common_py.compare_orderable_list(l1, l1))
        self.assertFalse(common_py.compare_orderable_list(l1, l2))
        self.assertFalse(common_py.compare_orderable_list(l1, l3))


class TestListDiff(unittest.TestCase):
    def test_list_diff_success(self):
        self.assertEqual(common_py.list_diff([1, 2, 3, 4], [1, 2, 3]), [4])
        self.assertEqual(common_py.list_diff([1, 2, 3], [1, 2, 3, 4]), [])
        self.assertEqual(common_py.list_diff([1, 2, 3, 4, 4], [1, 2, 3]), [4])
        self.assertEqual(common_py.list_diff([1, 2, 3, 4, 4], [1, 2, 3, 3, 3]), [4])


class TestListIntersection(unittest.TestCase):
    def test_list_intersection_success(self):
        self.assertEqual(common_py.list_intersection([1, 2, 3], [1, 5, 9, 2]), [1, 2])
        self.assertEqual(
            common_py.list_intersection([1, 2, 3, 3, 3, 2], [1, 5, 9, 2]), [1, 2]
        )
