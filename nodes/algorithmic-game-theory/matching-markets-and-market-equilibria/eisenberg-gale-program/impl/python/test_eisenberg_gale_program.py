# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eisenberg-gale-program/. The authors are listed in prov/R0QFZC.jsonl.

import math
import random
import unittest
from fractions import Fraction
from itertools import combinations

from eisenberg_gale_program import eisenberg_gale, objective, prices_from_support

# The example of the page: 3 buyers and 2 goods.
EXAMPLE_U = [[2, 1], [1, 2], [1, 1]]
EXAMPLE_E = [1, 1, 2]


def is_equilibrium(u, e, p, x):
    """Exact KKT check, with x in amounts of goods: positive prices, every good sold out, every
    buyer spends exactly her budget and only on goods of maximum bang per buck."""
    n, m = len(u), len(u[0])
    if any(q <= 0 for q in p):
        return False
    for j in range(m):
        if sum(x[i][j] for i in range(n)) != 1:
            return False
    for i in range(n):
        best = max(Fraction(u[i][j]) / p[j] for j in range(m))
        if sum(p[j] * x[i][j] for j in range(m)) != e[i]:
            return False
        for j in range(m):
            if x[i][j] < 0 or (x[i][j] > 0 and Fraction(u[i][j]) / p[j] != best):
                return False
    return True


def brute_force_prices(u, e):
    """Every price vector forced by some set of edges that passes the check with a forest flow."""
    n, m = len(u), len(u[0])
    all_edges = [(i, j) for i in range(n) for j in range(m) if u[i][j] > 0]
    found = set()
    for k in range(1, len(all_edges) + 1):
        for H in combinations(all_edges, k):
            if k > n + m - 1:
                continue
            p = prices_from_support(u, e, H)
            if p is None or None in p:
                continue
            x = forest_flow(n, m, e, p, H)
            if x is not None and is_equilibrium(u, e, p, x):
                found.add(tuple(p))
    return found


def forest_flow(n, m, e, p, H):
    left = set(H)
    need = {("b", i): Fraction(e[i]) for i in range(n)}
    need.update({("g", j): p[j] for j in range(m)})
    x = [[Fraction(0)] * m for _ in range(n)]
    while left:
        deg = {}
        for i, j in left:
            deg[("b", i)] = deg.get(("b", i), 0) + 1
            deg[("g", j)] = deg.get(("g", j), 0) + 1
        leaf = next((v for v, d in deg.items() if d == 1), None)
        if leaf is None:
            return None
        i, j = next(ed for ed in left if ("b", ed[0]) == leaf or ("g", ed[1]) == leaf)
        if need[leaf] < 0:
            return None
        x[i][j] = need[leaf] / p[j]
        need[("b", i)] -= need[leaf]
        need[("g", j)] -= p[j] * x[i][j]
        left.discard((i, j))
    return x if all(v == 0 for v in need.values()) else None


def random_market(rng, n, m):
    while True:
        u = [[rng.choice([0, 1, 2, 3, 4]) for _ in range(m)] for _ in range(n)]
        if all(any(r) for r in u) and all(any(u[i][j] for i in range(n)) for j in range(m)):
            return u, [rng.randint(1, 3) for _ in range(n)]


class TestEisenbergGale(unittest.TestCase):
    def test_check_value(self):
        p, x = eisenberg_gale([[2, 1], [1, 2]], [1, 1])
        self.assertEqual(p, [1, 1])
        self.assertEqual(x, [[1, 0], [0, 1]])

    def test_example(self):
        p, x = eisenberg_gale(EXAMPLE_U, EXAMPLE_E)
        self.assertEqual(p, [2, 2])
        self.assertTrue(is_equilibrium(EXAMPLE_U, EXAMPLE_E, p, x))
        # Buyer 1 buys only good 1 and buyer 2 only good 2; buyer 3 takes the rest.
        self.assertEqual(x[0], [Fraction(1, 2), 0])
        self.assertEqual(x[1], [0, Fraction(1, 2)])

    def test_random_against_brute_force(self):
        rng = random.Random(3)
        for _ in range(25):
            n, m = rng.randint(1, 3), rng.randint(1, 3)
            u, e = random_market(rng, n, m)
            p, x = eisenberg_gale(u, e)
            self.assertTrue(is_equilibrium(u, e, p, x))
            self.assertEqual(brute_force_prices(u, e), {tuple(p)})

    def test_optimal_against_random_points(self):
        rng = random.Random(5)
        for _ in range(10):
            u, e = random_market(rng, 3, 3)
            p, x = eisenberg_gale(u, e)
            best = objective(u, e, [[float(v) for v in row] for row in x])
            for _ in range(200):
                y = [[rng.random() * (u[i][j] > 0) for j in range(3)] for i in range(3)]
                for j in range(3):
                    s = sum(y[i][j] for i in range(3))
                    for i in range(3):
                        y[i][j] /= s
                if all(sum(u[i][j] * y[i][j] for j in range(3)) > 0 for i in range(3)):
                    self.assertLessEqual(objective(u, e, y), best + 1e-9)

    def test_identical_buyers(self):
        # Prices are unique, but the allocation is not: any split that spends both budgets works.
        p, x = eisenberg_gale([[1, 1], [1, 1]], [1, 1])
        self.assertEqual(p, [1, 1])
        self.assertTrue(is_equilibrium([[1, 1], [1, 1]], [1, 1], p, x))
        self.assertTrue(math.isclose(objective([[1, 1], [1, 1]], [1, 1], [[1, 0], [0, 1]]), 0.0))


if __name__ == "__main__":
    unittest.main()
