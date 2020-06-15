from typing import Dict
import unittest

import common_py


class TestGetOrElse(unittest.TestCase):
    def test_get_or_else_success(self):
        dict: Dict[str, str] = {
            "apple": "computer",
            "orange": "fruit",
            "carrot": "bait",
        }
        self.assertEqual(common_py.get_or_else(dict, "apple"), "computer")
        self.assertEqual(common_py.get_or_else(dict, "axe", "no value"), "no value")
        self.assertEqual(common_py.get_or_else(dict, "orange", "no value"), "fruit")
