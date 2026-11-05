# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-decomposition-construction/. The authors are listed in prov/EC5HWV.jsonl.
import random
import unittest
from functools import lru_cache

from tree_decomposition_construction import is_tree_decomposition, tree_decomposition


def exact_treewidth(n, edges):
    """Oracle: dynamic programming over vertex subsets and elimination orders."""
    if n == 0:
        return -1
    adj = [0] * n
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    def q(s, v):
        # vertices outside s + v reachable from v through vertices of s
        seen = 1 << v
        frontier = [v]
        out = 0
        while frontier:
            u = frontier.pop()
            nb = adj[u] & ~seen
            seen |= nb
            out |= nb & ~s
            inside = nb & s
            while inside:
                low = inside & -inside
                frontier.append(low.bit_length() - 1)
                inside ^= low
        return bin(out).count("1")

    @lru_cache(maxsize=None)
    def tw(s):
        if s == 0:
            return -1
        best = n
        rest = s
        while rest:
            low = rest & -rest
            v = low.bit_length() - 1
            rest ^= low
            best = min(best, max(tw(s ^ low), q(s ^ low, v)))
        return best

    return tw((1 << n) - 1)


def width(bags):
    return max(len(b) for b in bags) - 1


def random_graph(n, rng):
    p = rng.choice([0.15, 0.3, 0.5])
    return [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]


def partial_k_tree(n, k, rng):
    """A random subgraph of a random k-tree: treewidth at most k."""
    base = list(range(min(n, k + 1)))
    edges = {(u, v) for u in base for v in base if u < v}
    cliques = [[w for w in base if w != d] for d in base]
    for v in range(k + 1, n):
        c = rng.choice(cliques)
        edges.update((u, v) for u in c)
        cliques.extend([w for w in c if w != d] + [v] for d in c)
    return [e for e in sorted(edges) if rng.random() < 0.8]


class TestTreeDecomposition(unittest.TestCase):
    def check(self, n, edges, k):
        res = tree_decomposition(n, edges, k)
        if res is not None:
            bags, tree_edges = res
            self.assertTrue(is_tree_decomposition(n, edges, bags, tree_edges))
            self.assertLessEqual(width(bags), 4 * k + 4)
        return res

    def test_page_example(self):
        # the triangle strip: treewidth 2
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
        self.assertIsNotNone(self.check(6, edges, 2))
        self.assertIsNone(tree_decomposition(6, edges, 0))
        self.assertEqual(exact_treewidth(6, edges), 2)

    def test_small(self):
        self.assertEqual(tree_decomposition(1, [], 0), ([[0]], []))
        self.assertIsNotNone(self.check(2, [(0, 1)], 1))
        self.assertIsNone(tree_decomposition(2, [(0, 1)], 0))
        k5 = [(u, v) for u in range(5) for v in range(u + 1, 5)]
        self.assertIsNone(tree_decomposition(5, k5, 1))
        self.assertIsNotNone(self.check(5, k5, 4))

    def test_star(self):
        n = 50
        self.assertIsNotNone(self.check(n, [(0, v) for v in range(1, n)], 1))

    def test_long_path(self):
        n = 3000  # deeper than the default recursion limit
        edges = [(v, v + 1) for v in range(n - 1)]
        bags, tree_edges = tree_decomposition(n, edges, 1)
        self.assertTrue(is_tree_decomposition(n, edges, bags, tree_edges))

    def test_grid_fails(self):
        # the 4 by 4 grid has treewidth 4
        idx = lambda r, c: 4 * r + c
        edges = [(idx(r, c), idx(r, c + 1)) for r in range(4) for c in range(3)]
        edges += [(idx(r, c), idx(r + 1, c)) for r in range(3) for c in range(4)]
        self.assertIsNone(tree_decomposition(16, edges, 0))
        self.assertIsNotNone(self.check(16, edges, 4))

    def test_spider_uses_separators(self):
        # tips 0..8 are taken first, so a bag boundary of size 3k+4 = 7 appears
        legs = 9
        n = 2 * legs + 1
        edges = [(i, legs + i) for i in range(legs)] + [(legs + i, n - 1) for i in range(legs)]
        self.assertIsNotNone(self.check(n, edges, 1))

    def test_bounded_treewidth_never_fails(self):
        rng = random.Random(1187)
        for _ in range(120):
            k = rng.choice([1, 2])
            n = rng.randint(10, 35)
            edges = partial_k_tree(n, k, rng)
            perm = list(range(n))
            rng.shuffle(perm)
            edges = [(perm[u], perm[v]) for u, v in edges]
            self.assertIsNotNone(self.check(n, edges, k))
        self.check(16, [(4 * r + c, 4 * r + c + 1) for r in range(4) for c in range(3)]
                   + [(4 * r + c, 4 * r + c + 4) for r in range(3) for c in range(4)], 1)

    def test_random_against_oracle(self):
        rng = random.Random(7041)
        for _ in range(600):
            n = rng.randint(1, 9)
            edges = random_graph(n, rng)
            tw = exact_treewidth(n, edges)
            k = rng.randint(0, 3)
            res = self.check(n, edges, k)
            if tw <= k:
                self.assertIsNotNone(res)
            if res is None:
                self.assertGreater(tw, k)


if __name__ == "__main__":
    unittest.main()
