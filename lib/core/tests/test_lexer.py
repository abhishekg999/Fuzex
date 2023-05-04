import os
import sys

sys.path.insert(0, "..")

import unittest
from unittest import TestCase
import logging

from lexer import *


class TestLexer(TestCase):
    static_ex = [r"1234", r"12\$34a", "\$\[\]\(\)\(\(\(", r"\\"]
    static_ex_size = [4, 6, 8, 1]

    def test_static(self):
        for e, s in zip(self.static_ex, self.static_ex_size):
            L = Lexer(e)
            self.assertEqual(len(L), s, f"Expected size {s} on input {e}, got {len(L)}")


if __name__ == "__main__":
    unittest.main()
