# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-min-max-tree/. The authors are listed in prov/EHY1SS.jsonl.
"""Tests for the range min-max tree."""

from __future__ import annotations

import random
import unittest
from typing import Optional

from range_min_max_tree import RangeMinMaxTree

EXAMPLE = "((()())()((())))"


def random_balanced(rng: random.Random, n: int) -> list[int]:
    """A random balanced sequence of n pairs, built from a random tree."""
    ch: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        ch[rng.randrange(v)].append(v)
    out: list[int] = []

    def walk(v: int) -> None:
        out.append(1)
        for c in ch[v]:
            walk(c)
        out.append(0)

    walk(0)
    return out


def excess_list(p: list[int]) -> list[int]:
    e, out = 0, []
    for x in p:
        e += 1 if x else -1
        out.append(e)
    return out


def naive_fwd(E: list[int], i: int, d: int) -> Optional[int]:
    for j in range(i + 1, len(E)):
        if E[j] == E[i] + d:
            return j
    return None


def naive_bwd(E: list[int], i: int, d: int) -> Optional[int]:
    for j in range(i - 1, -2, -1):
        if (E[j] if j >= 0 else 0) == E[i] + d:
            return j
    return None


class TestRmM(unittest.TestCase):
    def test_example(self) -> None:
        t = RangeMinMaxTree(EXAMPLE, b=4)
        self.assertEqual(t.e[t.size:t.size + 4], [2, 0, 2, -4])
        self.assertEqual(t.m[t.size:t.size + 4], [1, -1, -1, -4])
        self.assertEqual(t.M[t.size:t.size + 4], [3, 1, 2, -1])
        self.assertEqual((t.e[1], t.m[1], t.M[1]), (0, 0, 4))
        self.assertEqual((t.e[2], t.m[2], t.M[2]), (2, 1, 3))
        self.assertEqual((t.e[3], t.m[3], t.M[3]), (-2, -2, 2))
        self.assertEqual(t.findclose(1), 6)
        self.assertEqual(t.findclose(0), 15)
        self.assertEqual(t.findclose(9), 14)
        self.assertEqual(t.findopen(12), 11)
        self.assertEqual(t.findopen(15), 0)
        self.assertEqual(t.enclose(4), 1)
        self.assertEqual(t.enclose(11), 10)
        self.assertIsNone(t.enclose(0))
        self.assertEqual(t.rmq(4, 11), 6)
        self.assertEqual(t.min_excess(4, 11), 1)

    def test_tiny(self) -> None:
        t = RangeMinMaxTree("()", b=1)
        self.assertEqual(t.findclose(0), 1)
        self.assertEqual(t.findopen(1), 0)
        self.assertIsNone(t.enclose(0))

    def test_random(self) -> None:
        rng = random.Random(1155)
        for _ in range(500):
            p = random_balanced(rng, rng.randint(1, 40))
            t = RangeMinMaxTree(p, b=rng.choice([1, 2, 3, 4, 8, 16]))
            E = excess_list(p)
            N = len(p)
            for _ in range(8):
                i = rng.randrange(N)
                d = rng.randint(-4, 3)
                self.assertEqual(t.excess(i), E[i])
                self.assertEqual(t.fwdsearch(i, d), naive_fwd(E, i, d))
                self.assertEqual(t.bwdsearch(i, d), naive_bwd(E, i, d))
                a, z = sorted((rng.randrange(N), rng.randrange(N)))
                self.assertEqual(t.min_excess(a, z), min(E[a:z + 1]))
                self.assertEqual(t.rmq(a, z), a + E[a:z + 1].index(min(E[a:z + 1])))
            for i in range(N):
                if p[i]:
                    j = t.findclose(i)
                    self.assertEqual(t.findopen(j), i)


if __name__ == "__main__":
    unittest.main()
