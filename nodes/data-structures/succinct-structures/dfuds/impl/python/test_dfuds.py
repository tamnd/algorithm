# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dfuds/. The authors are listed in prov/BT52AM.jsonl.
"""Tests for DFUDS."""

from __future__ import annotations

import random
import unittest

from dfuds import DFUDS

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


class TestDFUDS(unittest.TestCase):
    def test_example(self) -> None:
        t = DFUDS(EXAMPLE)
        self.assertEqual(t.text(), "(((()(())))()())")
        pos = {v: t.node_at(k) for k, v in enumerate(t.order)}
        self.assertEqual([pos[x] for x in range(8)], [1, 5, 10, 11, 8, 9, 13, 15])
        A, B, C, D, E, F, G, H = (pos[x] for x in range(8))
        self.assertEqual(t.degree(A), 3)
        self.assertEqual([t.child(A, i) for i in (1, 2, 3)], [B, C, D])
        self.assertIsNone(t.child(A, 4))
        self.assertEqual(t.parent(F), B)
        self.assertEqual(t.parent(D), A)
        self.assertIsNone(t.parent(A))
        self.assertEqual(t.child_rank(D), 3)
        self.assertEqual(t.subtree_size(D), 3)
        self.assertEqual(t.subtree_size(A), 8)
        self.assertEqual(t.next_sibling(E), F)
        self.assertIsNone(t.next_sibling(F))
        self.assertTrue(t.is_leaf(H))
        self.assertEqual(t.preorder_rank(C), 4)

    def test_single(self) -> None:
        t = DFUDS([[]])
        self.assertEqual(t.text(), "()")
        self.assertEqual(t.degree(1), 0)
        self.assertEqual(t.subtree_size(1), 1)
        self.assertIsNone(t.parent(1))

    def test_random(self) -> None:
        rng = random.Random(52)
        for _ in range(500):
            n = rng.randint(1, 30)
            ch = random_tree(rng, n)
            t = DFUDS(ch)
            self.assertEqual(len(t.U), 2 * n)
            pos = {v: t.node_at(k) for k, v in enumerate(t.order)}
            par = {c: v for v in range(n) for c in ch[v]}
            size = [1] * n
            for v in reversed(t.order):
                if v in par:
                    size[par[v]] += size[v]
            for v in range(n):
                x = pos[v]
                self.assertEqual(t.preorder_rank(x), t.order.index(v))
                self.assertEqual(t.degree(x), len(ch[v]))
                self.assertEqual(t.is_leaf(x), not ch[v])
                self.assertEqual([t.child(x, i) for i in range(1, len(ch[v]) + 1)], [pos[c] for c in ch[v]])
                self.assertEqual(t.subtree_size(x), size[v])
                if v in par:
                    self.assertEqual(t.parent(x), pos[par[v]])
                    sib = ch[par[v]]
                    k = sib.index(v)
                    self.assertEqual(t.child_rank(x), k + 1)
                    self.assertEqual(t.next_sibling(x), pos[sib[k + 1]] if k + 1 < len(sib) else None)
                else:
                    self.assertIsNone(t.parent(x))


if __name__ == "__main__":
    unittest.main()
