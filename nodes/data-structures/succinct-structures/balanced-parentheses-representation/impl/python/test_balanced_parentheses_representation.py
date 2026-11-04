# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-parentheses-representation/. The authors are listed in prov/8WYTP6.jsonl.
"""Tests for the BP tree."""

from __future__ import annotations

import random
import unittest

from balanced_parentheses_representation import BPTree

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


class TestBP(unittest.TestCase):
    def test_example(self) -> None:
        t = BPTree(EXAMPLE)
        self.assertEqual(t.text(), "((()())()((())))")
        pos = {t.order[r]: i for r, i in enumerate(i for i, b in enumerate(t.P) if b)}
        A, B, C, D, E, F, G, H = (pos[x] for x in range(8))
        self.assertEqual([A, B, E, F, C, D, G, H], [0, 1, 2, 4, 7, 9, 10, 11])
        self.assertEqual(t.first_child(B), E)
        self.assertIsNone(t.first_child(E))
        self.assertEqual(t.next_sibling(B), C)
        self.assertIsNone(t.next_sibling(D))
        self.assertEqual(t.parent(F), B)
        self.assertEqual(t.parent(H), G)
        self.assertIsNone(t.parent(A))
        self.assertEqual(t.subtree_size(D), 3)
        self.assertEqual(t.subtree_size(A), 8)
        self.assertEqual(t.depth(H), 3)
        self.assertTrue(t.is_ancestor(D, H))
        self.assertFalse(t.is_ancestor(B, H))
        self.assertEqual(t.lca(E, F), B)
        self.assertEqual(t.lca(F, H), A)
        self.assertEqual(t.lca(G, H), G)
        self.assertEqual(t.preorder_rank(C), 4)
        self.assertEqual(t.degree(A), 3)

    def test_single(self) -> None:
        t = BPTree([[]])
        self.assertEqual(t.text(), "()")
        self.assertIsNone(t.first_child(0))
        self.assertIsNone(t.next_sibling(0))
        self.assertIsNone(t.parent(0))
        self.assertEqual(t.subtree_size(0), 1)

    def test_random(self) -> None:
        rng = random.Random(8)
        for _ in range(500):
            n = rng.randint(1, 30)
            ch = random_tree(rng, n)
            t = BPTree(ch)
            opens = [i for i, b in enumerate(t.P) if b]
            pos = {t.order[r]: i for r, i in enumerate(opens)}
            par = {c: v for v in range(n) for c in ch[v]}
            depth = {0: 0}
            size = [1] * n
            for v in t.order:
                for c in ch[v]:
                    depth[c] = depth[v] + 1
            for v in reversed(t.order):
                if v in par:
                    size[par[v]] += size[v]
            for v in range(n):
                x = pos[v]
                self.assertEqual(t.preorder_rank(x), t.order.index(v))
                self.assertEqual(t.first_child(x), pos[ch[v][0]] if ch[v] else None)
                self.assertEqual(t.parent(x), pos[par[v]] if v in par else None)
                self.assertEqual(t.subtree_size(x), size[v])
                self.assertEqual(t.depth(x), depth[v])
                self.assertEqual(t.degree(x), len(ch[v]))
                if v in par:
                    sib = ch[par[v]]
                    k = sib.index(v)
                    self.assertEqual(t.next_sibling(x), pos[sib[k + 1]] if k + 1 < len(sib) else None)
            anc = {v: {v} for v in range(n)}
            for v in t.order:
                if v in par:
                    anc[v] = anc[par[v]] | {v}
            for _ in range(10):
                a, b = rng.randrange(n), rng.randrange(n)
                common = anc[a] & anc[b]
                want = max(common, key=lambda z: depth[z])
                self.assertEqual(t.lca(pos[a], pos[b]), pos[want])
                self.assertEqual(t.is_ancestor(pos[a], pos[b]), a in anc[b])


if __name__ == "__main__":
    unittest.main()
