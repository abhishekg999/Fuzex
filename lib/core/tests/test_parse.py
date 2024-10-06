import os
import sys

sys.path.insert(0, "..")

import unittest
from unittest import TestCase

from parse import *


class TestParse(TestCase):
    static_ex = [r"1234", r"12\$34a", r"\$\[\]\(\)\(\(\(", r"\\"]
    static_ex_size = [1, 1, 1, 1]
    static_ex_out = [[r"1234"], [r"12$34a"], [r"$[]()((("], ["\\"]]

    raw_dynamic_ex = [r"11[a-z]", r"[123abc][qwerty]", r"[aaa]", r"[a]", r"[\$\[]"]
    raw_dynamic_ex_size = [26, 36, 1, 1, 2]
    raw_dynamic_ex_out = [
        sorted(["11" + chr(i) for i in range(ord("a"), ord("z") + 1)]),
        sorted([x + y for x in "123abc" for y in "qwerty"]),
        sorted(["a"]),
        sorted(["a"]),
        sorted(["$", "["]),
    ]

    def test_static(self):
        for e, s, o in zip(self.static_ex, self.static_ex_size, self.static_ex_out):
            P = Parser(e)
            exp = P.parse()
            self.assertEqual(exp.size(), s, f"Expected size {s}.")

            i = 0
            for out in exp.generate():
                self.assertEqual(out, o[i], f"Expected value {o[i]}.")
                i += 1

            self.assertEqual(i, s, f"Expected size {s}, generated only {i}.")

    def test_dynamic(self):
        for e, s, o in zip(
            self.raw_dynamic_ex, self.raw_dynamic_ex_size, self.raw_dynamic_ex_out
        ):
            P = Parser(e)
            exp = P.parse()

            self.assertEqual(exp.size(), s, f"Expected size {s} on input {e}.")

            output = sorted([out for out in exp.generate()])

            self.assertEqual(output, o, f"Expected value {output} on input {e}.")
            self.assertEqual(
                len(output),
                s,
                f"Expected size {s}, generated only {len(output)} on input {e}.",
            )


if __name__ == "__main__":
    unittest.main()
