# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mex-function/. The authors are listed in prov/0H0WG2.jsonl.

import random
import sys
import unittest

from mex_function import grundy, mex, mex_naive, subtraction_grundy

sys.setrecursionlimit(10000)


class TestMex(unittest.TestCase):
    def test_small_sets(self):
        self.assertEqual(mex([]), 0)
        self.assertEqual(mex([1, 2]), 0)
        self.assertEqual(mex([0, 1, 3]), 2)
        self.assertEqual(mex([0, 2]), 1)
        self.assertEqual(mex([0, 1, 2]), 3)
        self.assertEqual(mex([0, 0, 0, 1]), 2)
        self.assertEqual(mex([5, 0, 100, 1, 2]), 3)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            mex([0, -1])

    def test_random_against_definition(self):
        rng = random.Random(20261113)
        for _ in range(3000):
            k = rng.randint(0, 12)
            s = [rng.randint(0, 15) for _ in range(k)]
            m = mex(s)
            self.assertEqual(m, mex_naive(s))
            self.assertNotIn(m, s)
            self.assertTrue(all(v in s for v in range(m)))
            self.assertLessEqual(m, len(set(s)))


class TestGrundy(unittest.TestCase):
    N = 200

    def recursive(self, moves, n):
        return grundy(n, lambda h: [h - m for m in moves if m <= h])

    def test_take_one_or_two(self):
        for n in range(self.N + 1):
            self.assertEqual(self.recursive((1, 2), n), n % 3)

    def test_take_one_two_or_three(self):
        for n in range(self.N + 1):
            self.assertEqual(self.recursive((1, 2, 3), n), n % 4)

    def test_take_one_three_or_four(self):
        period = [0, 1, 0, 1, 2, 3, 2]
        for n in range(self.N + 1):
            self.assertEqual(self.recursive((1, 3, 4), n), period[n % 7])

    def test_table_matches_recursion(self):
        for moves in ((1, 2), (1, 2, 3), (1, 3, 4), (2, 3), (2, 5, 7)):
            table = subtraction_grundy(moves, self.N)
            for n in range(self.N + 1):
                self.assertEqual(table[n], self.recursive(moves, n))

    def test_nim_heap(self):
        for n in range(60):
            self.assertEqual(grundy(n, lambda h: range(h)), n)


if __name__ == "__main__":
    unittest.main()
