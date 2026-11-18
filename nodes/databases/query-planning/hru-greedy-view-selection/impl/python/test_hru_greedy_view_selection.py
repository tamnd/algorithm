# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hru-greedy-view-selection/. The authors are listed in prov/TY6PHM.jsonl.

import math
import unittest
from itertools import combinations
from random import Random

from hru_greedy_view_selection import (
    Lattice,
    best_k_views,
    best_within_space,
    cube_lattice,
    greedy_bound,
    greedy_per_space,
    greedy_views,
)


def example_4_1():
    """The lattice of Example 4.1 (Fig. 7) of Harinarayan, Rajaraman and Ullman."""
    sizes = {"a": 100, "b": 50, "c": 75, "d": 20, "e": 30, "f": 40, "g": 1, "h": 10}
    edges = [("a", "b"), ("a", "c"), ("b", "d"), ("b", "e"), ("c", "e"), ("c", "f"),
             ("d", "g"), ("e", "g"), ("e", "h"), ("f", "h")]
    return Lattice(sizes, edges, "a")


def example_4_2():
    """The lattice of Example 4.2 (Fig. 9): four chains of 20 views under b, c and d."""
    sizes = {"a": 200, "b": 100, "c": 99, "d": 100}
    edges = [("a", "b"), ("a", "c"), ("a", "d")]
    heads = []
    for chain in range(4):
        prev = None
        for i in range(20):
            v = "x%d_%02d" % (chain, i)
            sizes[v] = 100
            if prev is not None:
                edges.append((prev, v))
            else:
                heads.append(v)
            prev = v
    for parent, chain in [("b", 0), ("b", 1), ("c", 1), ("c", 2), ("d", 2), ("d", 3)]:
        edges.append((parent, heads[chain]))
    return Lattice(sizes, edges, "a")


def random_cube(rng, d):
    dims = "pqrs"[:d]
    dom = {x: rng.choice([2, 3, 5, 10, 20, 50]) for x in dims}
    top = rng.randint(200, 3000)

    def size_of(s):
        return min(top, math.prod(dom[x] for x in s)) if s else 1

    return cube_lattice(dims, size_of)


def random_dag(rng, n):
    """A random lattice-like order: view 0 on top, edges from lower to higher numbers."""
    sizes = {0: 1000}
    edges = []
    for v in range(1, n):
        parents = rng.sample(range(v), rng.randint(1, min(3, v)))
        edges += [(p, v) for p in parents]
        sizes[v] = rng.randint(1, min(sizes[p] for p in parents))
    return Lattice(sizes, edges, 0)


class TestExamples(unittest.TestCase):
    def test_example_4_1(self):
        lat = example_4_1()
        self.assertEqual(lat.total_cost([]), 800)
        picks, gains = greedy_views(lat, 3)
        self.assertEqual(picks, ["b", "f", "d"])
        self.assertEqual(gains, [250, 70, 60])
        self.assertEqual(lat.total_cost(picks), 420)
        self.assertEqual(best_k_views(lat, 3)[0], 380)

    def test_example_4_1_rounds(self):
        lat = example_4_1()
        from hru_greedy_view_selection import _benefit
        cost = lat.costs([])
        r1 = {v: _benefit(lat, cost, v) for v in "bcdefgh"}
        self.assertEqual(r1, {"b": 250, "c": 125, "d": 160, "e": 210, "f": 120, "g": 99, "h": 90})
        cost = lat.costs(["b"])
        r2 = {v: _benefit(lat, cost, v) for v in "cdefgh"}
        self.assertEqual(r2, {"c": 50, "d": 60, "e": 60, "f": 70, "g": 49, "h": 40})
        cost = lat.costs(["b", "f"])
        r3 = {v: _benefit(lat, cost, v) for v in "cdegh"}
        self.assertEqual(r3, {"c": 25, "d": 60, "e": 50, "g": 49, "h": 30})

    def test_example_4_2(self):
        lat = example_4_2()
        picks, gains = greedy_views(lat, 2)
        self.assertEqual(picks[0], "c")
        self.assertEqual(gains, [4141, 2100])
        best, chosen = best_k_views(lat, 2)
        self.assertEqual(best, 8200)
        self.assertEqual(set(chosen), {"b", "d"})
        self.assertGreaterEqual(sum(gains) / best, greedy_bound(2))

    def test_bound_values(self):
        self.assertEqual(greedy_bound(1), 1)
        self.assertEqual(greedy_bound(2), 0.75)
        self.assertGreater(greedy_bound(50), 1 - 1 / math.e)


class TestGuarantee(unittest.TestCase):
    def check(self, lat, k):
        picks, gains = greedy_views(lat, k)
        self.assertAlmostEqual(sum(gains), lat.benefit_of_set(picks))
        opt = best_k_views(lat, k)[0]
        self.assertGreaterEqual(sum(gains) + 1e-9, greedy_bound(k) * opt)
        self.assertLessEqual(sum(gains), opt + 1e-9)
        return sum(gains), opt

    def test_cubes(self):
        rng = Random(2)
        for _ in range(25):
            lat = random_cube(rng, rng.choice([3, 4]))
            for k in range(1, 4):
                self.check(lat, k)

    def test_random_orders(self):
        rng = Random(9)
        worse = 0
        for _ in range(30):
            lat = random_dag(rng, rng.randint(5, 11))
            for k in range(1, 4):
                g, opt = self.check(lat, k)
                worse += g < opt - 1e-9
        self.assertGreater(worse, 0)

    def test_weights(self):
        rng = Random(4)
        for _ in range(20):
            lat = random_cube(rng, 3)
            lat.weight = {v: rng.randint(0, 5) for v in lat.views}
            for k in range(1, 4):
                self.check(lat, k)

    def test_gains_do_not_grow(self):
        rng = Random(6)
        for _ in range(20):
            lat = random_dag(rng, 12)
            gains = greedy_views(lat, 6)[1]
            for x, y in zip(gains, gains[1:]):
                self.assertGreaterEqual(x, y)


class TestPerSpace(unittest.TestCase):
    def test_space_bound(self):
        rng = Random(8)
        for trial in range(20):
            lat = random_cube(rng, 3) if trial % 2 else random_dag(rng, 9)
            others = [v for v in lat.views if v != lat.top]
            table = []
            for m in range(1, len(others) + 1):
                for c in combinations(others, m):
                    table.append((sum(lat.size[v] for v in c), lat.benefit_of_set(c)))
            for v, space, total in greedy_per_space(lat):
                best = max([b for s, b in table if s <= space] + [0])
                self.assertGreaterEqual(total + 1e-9, (1 - 1 / math.e) * best)

    def test_brute_force_helper(self):
        lat = example_4_1()
        # d and e (space 20 + 30) save 160 + 140, more than b alone (250).
        self.assertEqual(best_within_space(lat, 50), 300)


if __name__ == "__main__":
    unittest.main()
