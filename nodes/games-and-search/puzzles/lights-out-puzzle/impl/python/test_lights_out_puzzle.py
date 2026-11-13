# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lights-out-puzzle/. The authors are listed in prov/XKXX36.jsonl.
import random
import unittest
from collections import Counter
from itertools import combinations

from lights_out_puzzle import (
    brute_force,
    effect,
    eliminate,
    fewest_presses,
    graph_masks,
    light_chasing,
    press_masks,
    rank,
    solve,
)


def popcount(x):
    return bin(x).count("1")


class TestAgainstBruteForce(unittest.TestCase):
    def test_solvable_sets(self):
        for r, c in ((1, 1), (1, 4), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)):
            masks = press_masks(r, c)
            n = r * c
            images = Counter(effect(masks, x) for x in range(1 << n))
            rk = rank(r, c)
            self.assertEqual(len(images), 2 ** rk)
            self.assertEqual(set(images.values()), {2 ** (n - rk)})
            for b in range(1 << n):
                s = solve(r, c, b)
                self.assertEqual(s is not None, b in images, (r, c, b))
                if s is not None:
                    self.assertEqual(effect(masks, s), b)

    def test_solution_counts(self):
        rnd = random.Random(7)
        for r, c in ((3, 3), (4, 4)):
            for _ in range(20):
                b = rnd.getrandbits(r * c)
                sols = brute_force(r, c, b)
                _, rk, basis = eliminate(press_masks(r, c), b)
                if sols:
                    self.assertEqual(len(sols), 2 ** len(basis))
                    best = fewest_presses(r, c, b)
                    self.assertEqual(popcount(best), min(popcount(x) for x in sols))
                else:
                    self.assertIsNone(solve(r, c, b))


class TestFiveByFive(unittest.TestCase):
    def test_rank_23(self):
        self.assertEqual(rank(5, 5), 23)

    def test_quiet_patterns(self):
        masks = press_masks(5, 5)
        _, _, basis = eliminate(masks, 0)
        self.assertEqual(len(basis), 2)
        for q in basis:
            self.assertEqual(effect(masks, q), 0)

    def test_solvable_iff_orthogonal(self):
        masks = press_masks(5, 5)
        _, _, basis = eliminate(masks, 0)
        rnd = random.Random(3)
        for _ in range(300):
            b = rnd.getrandbits(25)
            ok = all(popcount(b & q) % 2 == 0 for q in basis)
            self.assertEqual(solve(5, 5, b) is not None, ok)

    def test_all_on(self):
        x = fewest_presses(5, 5, (1 << 25) - 1)
        self.assertEqual(popcount(x), 15)
        self.assertEqual(popcount(fewest_presses(3, 3, (1 << 9) - 1)), 5)


class TestRanks(unittest.TestCase):
    def test_nullity_table(self):
        self.assertEqual([n * n - rank(n, n) for n in range(1, 12)], [0, 0, 0, 4, 2, 0, 0, 0, 8, 0, 6])


class TestLightChasing(unittest.TestCase):
    def test_agrees_with_elimination(self):
        rnd = random.Random(11)
        for r in range(1, 9):
            for c in range(1, 9):
                masks = press_masks(r, c)
                for _ in range(10):
                    b = rnd.getrandbits(r * c)
                    if rnd.random() < 0.5:
                        b = effect(masks, rnd.getrandbits(r * c))
                    s = light_chasing(r, c, b)
                    self.assertEqual(s is None, solve(r, c, b) is None)
                    if s is not None:
                        self.assertEqual(effect(masks, s), b)


class TestAllOnAnyGraph(unittest.TestCase):
    """Sutner: on every graph, pressing can turn all lights from on to off."""

    def test_all_small_graphs(self):
        for n in range(1, 6):
            pairs = list(combinations(range(n), 2))
            for e in range(1 << len(pairs)):
                adj = [[] for _ in range(n)]
                for k, (u, v) in enumerate(pairs):
                    if e >> k & 1:
                        adj[u].append(v)
                        adj[v].append(u)
                x, _, _ = eliminate(graph_masks(adj), (1 << n) - 1)
                self.assertIsNotNone(x)

    def test_random_graphs_and_grids(self):
        rnd = random.Random(5)
        for _ in range(200):
            n = rnd.randint(1, 14)
            adj = [[] for _ in range(n)]
            for u, v in combinations(range(n), 2):
                if rnd.random() < 0.3:
                    adj[u].append(v)
                    adj[v].append(u)
            self.assertIsNotNone(eliminate(graph_masks(adj), (1 << n) - 1)[0])
        for n in range(1, 21):
            self.assertIsNotNone(solve(n, n, (1 << (n * n)) - 1))


if __name__ == "__main__":
    unittest.main()
