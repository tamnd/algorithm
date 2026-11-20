# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bird-rule/. The authors are listed in prov/7MY1TF.jsonl.
"""Tests for bird_rule: the worked example, the core property against a Kruskal oracle,
the spanning tree, and the failure of population monotonicity."""

import itertools
import random
import unittest
from fractions import Fraction as F

from bird_rule import bird, coalition_cost

EXAMPLE = [
    [0, 4, 5, 6],
    [4, 0, 2, 5],
    [5, 2, 0, 3],
    [6, 5, 3, 0],
]

NOT_MONOTONE = [
    [0, 8, 9, 7],
    [8, 0, 1, 8],
    [9, 1, 0, 4],
    [7, 8, 4, 0],
]


def kruskal(cost, nodes):
    """An independent oracle: Kruskal's algorithm with a union-find on the given nodes."""
    nodes = list(nodes)
    root = {v: v for v in nodes}

    def find(v):
        while root[v] != v:
            root[v] = root[root[v]]
            v = root[v]
        return v

    total = 0
    for w, u, v in sorted((cost[u][v], u, v) for u, v in itertools.combinations(nodes, 2)):
        ru, rv = find(u), find(v)
        if ru != rv:
            root[ru] = rv
            total += w
    return total


def random_matrix(rng, n, frac=False):
    c = [[0] * (n + 1) for _ in range(n + 1)]
    for u in range(n + 1):
        for v in range(u + 1, n + 1):
            w = F(rng.randint(1, 30), rng.randint(1, 4)) if frac else rng.randint(1, 9)
            c[u][v] = c[v][u] = w
    return c


def bird_on(cost, players):
    """Bird's rule on the subgame of the given players (with the source 0)."""
    nodes = [0] + list(players)
    sub = [[cost[a][b] for b in nodes] for a in nodes]
    x, _ = bird(sub)
    return {p: x[k + 1] for k, p in enumerate(players)}


class TestBirdRule(unittest.TestCase):
    def test_worked_example(self):
        x, parent = bird(EXAMPLE)
        self.assertEqual(x, [0, 4, 2, 3])
        self.assertEqual(parent, [None, 0, 1, 2])
        self.assertEqual(sum(x), 9)
        costs = {S: coalition_cost(EXAMPLE, S) for r in range(1, 4) for S in itertools.combinations([1, 2, 3], r)}
        self.assertEqual(costs, {(1,): 4, (2,): 5, (3,): 6, (1, 2): 6, (1, 3): 9, (2, 3): 8, (1, 2, 3): 9})

    def test_edge_cases(self):
        self.assertEqual(bird([[0]]), ([0], [None]))
        self.assertEqual(bird([[0, 7], [7, 0]]), ([0, 7], [None, 0]))
        x, parent = bird([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
        self.assertEqual((x, parent), ([0, 1, 1], [None, 0, 0]))
        with self.assertRaises(ValueError):
            bird([[0, 1], [2, 0]])
        with self.assertRaises(ValueError):
            bird([[0, 1], [1]])
        with self.assertRaises(ValueError):
            bird([])

    def test_core_and_tree_on_random_games(self):
        rng = random.Random(7)
        for trial in range(600):
            n = rng.randint(1, 6)
            c = random_matrix(rng, n, frac=trial % 3 == 0)
            x, parent = bird(c)
            players = range(1, n + 1)
            self.assertEqual(sum(x), kruskal(c, range(n + 1)))
            for v in players:
                self.assertEqual(x[v], c[parent[v]][v])
                seen, w = set(), v
                while w != 0:
                    self.assertNotIn(w, seen)
                    seen.add(w)
                    w = parent[w]
            for r in range(1, n + 1):
                for S in itertools.combinations(players, r):
                    cs = kruskal(c, (0,) + S)
                    self.assertEqual(coalition_cost(c, S), cs)
                    self.assertLessEqual(sum(x[i] for i in S), cs)

    def test_not_population_monotonic(self):
        small = bird_on(NOT_MONOTONE, [1, 2])
        full = bird_on(NOT_MONOTONE, [1, 2, 3])
        self.assertEqual(small, {1: 8, 2: 1})
        self.assertEqual(full, {1: 1, 2: 4, 3: 7})
        self.assertGreater(full[2], small[2])


if __name__ == "__main__":
    unittest.main()
