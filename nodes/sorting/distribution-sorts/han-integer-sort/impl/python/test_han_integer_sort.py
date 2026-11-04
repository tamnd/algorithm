# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/han-integer-sort/. The authors are listed in prov/0V80XQ.jsonl.
import random
import unittest

from han_integer_sort import han_integer_sort


class TestHanIntegerSort(unittest.TestCase):
    def test_page_example(self):
        a = [41, 7, 93, 18, 65, 30, 7, 88, 51, 24, 76, 3, 59, 12, 97, 35]
        self.assertEqual(a[::4], [41, 65, 51, 59])
        self.assertEqual(han_integer_sort(a, base=4), sorted(a))
        self.assertEqual(a[0], 41)

    def test_edges(self):
        for a in ([], [1], [2, 1], [5] * 50, [0, -5, 3, -1, -5, 2], [2**63 - 1, -(2**63), 0, -1, 1] * 4):
            self.assertEqual(han_integer_sort(a, base=2), sorted(a))

    def test_patterns(self):
        for a in (list(range(3000)), list(range(3000, 0, -1)), [i % 17 for i in range(3000)], [2**k for k in range(63)] * 5):
            self.assertEqual(han_integer_sort(a), sorted(a))

    def test_bad_base(self):
        with self.assertRaises(ValueError):
            han_integer_sort([2, 1], base=1)

    def test_random(self):
        rng = random.Random(2002)
        for _ in range(600):
            n = rng.randint(0, 150)
            hi = rng.choice([3, 1000, 2**64])
            a = [rng.randint(-hi, hi) for _ in range(n)]
            self.assertEqual(han_integer_sort(a, base=rng.choice([2, 4, 8])), sorted(a))


if __name__ == "__main__":
    unittest.main()
