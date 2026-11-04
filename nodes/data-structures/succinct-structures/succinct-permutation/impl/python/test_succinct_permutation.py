# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/succinct-permutation/. The authors are listed in prov/EAVGSD.jsonl.
"""Tests for the succinct permutation."""

from __future__ import annotations

import random
import unittest

from succinct_permutation import SuccinctPermutation

EXAMPLE = [3, 5, 7, 6, 0, 2, 1, 4, 8, 10, 9]


class CountingPerm(SuccinctPermutation):
    """Counts evaluations of pi made by inverse."""

    def inverse(self, i: int) -> int:
        pi = self.pi
        calls = [0]

        class Probe(list):
            def __getitem__(self, k):  # type: ignore[override]
                calls[0] += 1
                return list.__getitem__(self, k)

        self.pi = Probe(pi)
        try:
            r = super().inverse(i)
        finally:
            self.pi = pi
        self.last_calls = calls[0]
        return r


class TestSuccinctPermutation(unittest.TestCase):
    def test_example(self) -> None:
        p = SuccinctPermutation(EXAMPLE, t=3)
        self.assertEqual([i for i in range(11) if p.B[i]], [0, 1, 7])
        self.assertEqual(p.S, [7, 0, 1])
        self.assertEqual(p.inverse(2), 5)
        self.assertEqual(p.inverse(8), 8)
        self.assertEqual(p.inverse(9), 10)
        self.assertEqual(p.apply(2), 7)
        c = CountingPerm(EXAMPLE, t=3)
        self.assertEqual(c.inverse(2), 5)
        self.assertEqual(c.last_calls, 4)

    def test_edge(self) -> None:
        self.assertEqual(SuccinctPermutation([], t=2).n, 0)
        p = SuccinctPermutation([0], t=1)
        self.assertEqual(p.inverse(0), 0)
        with self.assertRaises(ValueError):
            SuccinctPermutation([0, 0])
        q = SuccinctPermutation([1, 2, 3, 0], t=1)
        self.assertEqual([q.inverse(i) for i in range(4)], [3, 0, 1, 2])

    def test_random(self) -> None:
        rng = random.Random(4096)
        for _ in range(600):
            n = rng.randint(1, 60)
            pi = list(range(n))
            rng.shuffle(pi)
            t = rng.randint(1, 8)
            c = CountingPerm(pi, t=t)
            inv = [0] * n
            for i, x in enumerate(pi):
                inv[x] = i
            for i in range(n):
                self.assertEqual(c.inverse(i), inv[i])
                self.assertLessEqual(c.last_calls, 2 * t + 1)
                self.assertEqual(c.apply(i), pi[i])
            self.assertLessEqual(c.extra_words(), n // t + n // (t + 1) + 1)


if __name__ == "__main__":
    unittest.main()
