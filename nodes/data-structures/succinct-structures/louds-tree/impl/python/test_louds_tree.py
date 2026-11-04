# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/louds-tree/. The authors are listed in prov/QA72X1.jsonl.
"""Tests for the LOUDS tree."""

from __future__ import annotations

import random
import unittest
from collections import deque

from louds_tree import LoudsTree

# A: B C D; B: E F; D: G; G: H  (input numbering A=0 .. H=7)
EXAMPLE = [[1, 2, 3], [4, 5], [], [6], [], [], [7], []]


def random_tree(rng: random.Random, n: int) -> list[list[int]]:
    """A random ordered tree on nodes 0..n-1 rooted at 0."""
    ch: list[list[int]] = [[] for _ in range(n)]
    for v in range(1, n):
        ch[rng.randrange(v)].append(v)
    for c in ch:
        rng.shuffle(c)
    return ch


def level_order(ch: list[list[int]]) -> list[int]:
    out, q = [], deque([0])
    while q:
        v = q.popleft()
        out.append(v)
        q.extend(ch[v])
    return out


class TestLouds(unittest.TestCase):
    def test_example(self) -> None:
        t = LoudsTree(EXAMPLE)
        self.assertEqual(t.bitstring(), "10111011001000100")
        self.assertEqual(t.degree(0), 3)
        self.assertEqual(t.child(0, 3), 3)
        self.assertEqual(t.child(1, 2), 5)
        self.assertEqual(t.parent(6), 3)
        self.assertEqual(t.next_sibling(1), 2)
        self.assertIsNone(t.next_sibling(3))
        self.assertEqual(t.child_rank(5), 2)
        self.assertIsNone(t.parent(0))
        self.assertIsNone(t.child(2, 1))
        self.assertTrue(t.is_leaf(7))

    def test_single_node(self) -> None:
        t = LoudsTree([[]])
        self.assertEqual(t.bitstring(), "100")
        self.assertEqual(t.degree(0), 0)
        self.assertIsNone(t.parent(0))
        self.assertIsNone(t.next_sibling(0))
        self.assertIsNone(t.prev_sibling(0))

    def test_path_and_star(self) -> None:
        path = [[1], [2], [3], []]
        t = LoudsTree(path)
        self.assertEqual(t.bitstring(), "101010100")
        self.assertEqual([t.parent(k) for k in range(1, 4)], [0, 1, 2])
        star = [[1, 2, 3, 4], [], [], [], []]
        s = LoudsTree(star)
        self.assertEqual(s.bitstring(), "10111100000")
        self.assertEqual([s.child_rank(k) for k in range(1, 5)], [1, 2, 3, 4])

    def test_random(self) -> None:
        rng = random.Random(72)
        for _ in range(500):
            n = rng.randint(1, 40)
            ch = random_tree(rng, n)
            t = LoudsTree(ch)
            order = level_order(ch)
            self.assertEqual(t.order, order)
            num = {v: k for k, v in enumerate(order)}
            self.assertEqual(len(t.bitstring()), 2 * n + 1)
            par = {c: v for v in range(n) for c in ch[v]}
            for v in range(n):
                k = num[v]
                self.assertEqual(t.degree(k), len(ch[v]))
                self.assertEqual(t.is_leaf(k), not ch[v])
                for i, c in enumerate(ch[v], 1):
                    self.assertEqual(t.child(k, i), num[c])
                self.assertIsNone(t.child(k, len(ch[v]) + 1))
                if v == 0:
                    self.assertIsNone(t.parent(k))
                    continue
                p = par[v]
                self.assertEqual(t.parent(k), num[p])
                idx = ch[p].index(v)
                self.assertEqual(t.child_rank(k), idx + 1)
                nxt = num[ch[p][idx + 1]] if idx + 1 < len(ch[p]) else None
                prv = num[ch[p][idx - 1]] if idx > 0 else None
                self.assertEqual(t.next_sibling(k), nxt)
                self.assertEqual(t.prev_sibling(k), prv)


if __name__ == "__main__":
    unittest.main()
