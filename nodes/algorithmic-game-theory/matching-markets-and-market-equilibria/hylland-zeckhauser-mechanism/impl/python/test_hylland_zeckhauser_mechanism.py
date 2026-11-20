# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hylland-zeckhauser-mechanism/. The authors are listed in prov/NMFNPQ.jsonl.

import random
import unittest
from fractions import Fraction as F

from agtlp import lp_max
from hylland_zeckhauser_mechanism import clearing_allocation, demand_values, hz_grid_search, is_equilibrium


def utility(ui, xi):
    return sum(a * b for a, b in zip(ui, xi))


def best_by_vertices(ui, p):
    """Best utility of a unit bundle with cost <= 1, by trying the vertices of the polytope."""
    m = len(p)
    best = None
    for j in range(m):
        if p[j] <= 1:
            best = ui[j] if best is None else max(best, ui[j])
        for k in range(m):
            if p[j] < 1 < p[k]:
                t = (p[k] - 1) / (p[k] - p[j])
                v = t * ui[j] + (1 - t) * ui[k]
                best = v if best is None else max(best, v)
    return best


def ex_ante_pareto_optimal(u, x):
    """LP check: no fractional allocation gives every agent as much and the total more."""
    n = len(u)
    nv = n * n
    A_eq, b_eq, A_ub, b_ub = [], [], [], []
    for i in range(n):
        A_eq.append([1 if v // n == i else 0 for v in range(nv)])
        b_eq.append(1)
    for j in range(n):
        A_eq.append([1 if v % n == j else 0 for v in range(nv)])
        b_eq.append(1)
    for i in range(n):
        A_ub.append([-u[i][v % n] if v // n == i else 0 for v in range(nv)])
        b_ub.append(-utility(u[i], x[i]))
    c = [u[v // n][v % n] for v in range(nv)]
    st, _, value, _ = lp_max(c, A_ub, b_ub, A_eq, b_eq)
    return st == "optimal" and value == sum(utility(u[i], x[i]) for i in range(n))


def uniform(n):
    return [[F(1, n)] * n for _ in range(n)]


class TestHyllandZeckhauser(unittest.TestCase):
    def test_identical_agents(self):
        u = [[3, 2, 0]] * 3
        p = [F(9, 5), F(6, 5), F(0)]
        self.assertTrue(is_equilibrium(u, p, uniform(3)))
        vals = [demand_values(u[i], p) for i in range(3)]
        self.assertEqual(vals[0], (F(5, 3), F(1)))
        x = clearing_allocation(u, p, vals)
        self.assertIsNotNone(x)
        self.assertTrue(is_equilibrium(u, p, x))
        for q in ([F(2), F(1), F(0)], [F(8, 5), F(7, 5), F(0)], [F(9, 5), F(6, 5), F(1, 5)]):
            self.assertFalse(is_equilibrium(u, q, uniform(3)))
            vals = [demand_values(u[i], q) for i in range(3)]
            self.assertIsNone(clearing_allocation(u, q, vals))

    def test_same_favourite(self):
        u = [[1, 0], [1, 0]]
        self.assertEqual(hz_grid_search(u), ([F(2), F(0)], uniform(2)))
        self.assertFalse(is_equilibrium(u, [F(1), F(0)], uniform(2)))
        self.assertTrue(ex_ante_pareto_optimal(u, uniform(2)))

    def test_different_favourites(self):
        u = [[2, 1], [1, 2]]
        p, x = hz_grid_search(u)
        self.assertEqual(p, [F(0), F(0)])
        self.assertEqual(x, [[1, 0], [0, 1]])

    def test_edge_cases(self):
        self.assertEqual(hz_grid_search([[5]]), ([F(0)], [[F(1)]]))
        with self.assertRaises(ValueError):
            hz_grid_search([[1, 2]])
        with self.assertRaises(ValueError):
            demand_values([1, 2], [F(2), F(3)])
        self.assertFalse(is_equilibrium([[1, 0], [1, 0]], [F(2), F(2)], uniform(2)))

    def test_demand_against_vertices(self):
        rng = random.Random(6)
        for _ in range(150):
            m = rng.randint(1, 4)
            ui = [rng.randint(0, 6) for _ in range(m)]
            p = [F(rng.randint(0, 12), rng.randint(1, 4)) for _ in range(m)]
            p[rng.randrange(m)] = F(rng.randint(0, 4), 4)  # some price is at most 1
            U, C = demand_values(ui, p)
            self.assertEqual(U, best_by_vertices(ui, p))
            self.assertLessEqual(C, 1)

    def test_random_two_agents(self):
        rng = random.Random(12)
        found = 0
        for _ in range(25):
            u = [[rng.randint(0, 4) for _ in range(2)] for _ in range(2)]
            res = hz_grid_search(u, k=4, pmax=2)
            if res is None:
                continue
            found += 1
            p, x = res
            self.assertTrue(is_equilibrium(u, p, x))
            self.assertTrue(ex_ante_pareto_optimal(u, x))
            for i in range(2):
                self.assertEqual(utility(u[i], x[i]), demand_values(u[i], p)[0])
                self.assertEqual(utility(u[i], x[i]), best_by_vertices(u[i], p))
                for k in range(2):  # envy-free: every bundle costs at most the budget 1
                    self.assertGreaterEqual(utility(u[i], x[i]), utility(u[i], x[k]))
        self.assertGreaterEqual(found, 20)


if __name__ == "__main__":
    unittest.main()
