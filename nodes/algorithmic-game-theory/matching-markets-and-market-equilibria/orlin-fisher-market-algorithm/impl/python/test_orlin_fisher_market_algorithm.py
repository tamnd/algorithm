# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orlin-fisher-market-algorithm/. The authors are listed in prov/XBSFVW.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations

from orlin_fisher_market_algorithm import orlin_scaling


def is_equilibrium(U, e, p, x):
    """Exact check with x in money: positive prices, budgets spent, goods sold, and money only on
    goods of maximum bang per buck."""
    nb, ng = len(U), len(U[0])
    if any(q <= 0 for q in p):
        return False
    for i in range(nb):
        best = max(Fraction(U[i][j]) / p[j] for j in range(ng))
        if sum(x[i]) != e[i]:
            return False
        if any(x[i][j] < 0 or (x[i][j] > 0 and Fraction(U[i][j]) / p[j] != best) for j in range(ng)):
            return False
    return all(sum(x[i][j] for i in range(nb)) == p[j] for j in range(ng))


def brute_force_prices(U, e):
    """All equilibrium prices, from every forest of spending edges: along a buyer's edges the bang
    per buck is equal, and on each tree the prices add up to the budgets."""
    nb, ng = len(U), len(U[0])
    edges = [(i, j) for i in range(nb) for j in range(ng) if U[i][j] > 0]
    found = set()
    for k in range(1, min(len(edges), nb + ng - 1) + 1):
        for H in combinations(edges, k):
            nodes = {("b", i) for i, _ in H} | {("g", j) for _, j in H}
            if len(nodes) != nb + ng or k != nb + ng - components(H):
                continue
            p = tree_prices(U, e, H)
            x = tree_flow(nb, ng, e, p, H)
            if x is not None and is_equilibrium(U, e, p, x):
                found.add(tuple(p))
    return found


def components(H):
    parent = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            a = parent[a]
        return a
    for i, j in H:
        parent[find(("b", i))] = find(("g", j))
    return len({find(a) for a in list(parent)})


def tree_prices(U, e, H):
    ng = len(U[0])
    rel = {}
    p = [None] * ng
    for j0 in range(ng):
        if ("g", j0) in rel:
            continue
        rel[("g", j0)] = Fraction(1)
        comp, changed = [("g", j0)], True
        while changed:
            changed = False
            for i, j in H:
                if ("g", j) in rel and ("b", i) not in rel:
                    rel[("b", i)] = Fraction(U[i][j]) / rel[("g", j)]
                elif ("b", i) in rel and ("g", j) not in rel:
                    rel[("g", j)] = Fraction(U[i][j]) / rel[("b", i)]
                else:
                    continue
                comp += [("b", i), ("g", j)]
                changed = True
        comp = set(comp)
        scale = sum(e[a[1]] for a in comp if a[0] == "b") / sum(rel[a] for a in comp if a[0] == "g")
        for a in comp:
            if a[0] == "g":
                p[a[1]] = rel[a] * scale
    return p


def tree_flow(nb, ng, e, p, H):
    left = set(H)
    need = {("b", i): Fraction(e[i]) for i in range(nb)}
    need.update({("g", j): p[j] for j in range(ng)})
    x = [[Fraction(0)] * ng for _ in range(nb)]
    while left:
        deg = {}
        for i, j in left:
            deg[("b", i)] = deg.get(("b", i), 0) + 1
            deg[("g", j)] = deg.get(("g", j), 0) + 1
        leaf = next(v for v, d in deg.items() if d == 1)
        i, j = next(ed for ed in left if ("b", ed[0]) == leaf or ("g", ed[1]) == leaf)
        if need[leaf] < 0:
            return None
        x[i][j] = need[leaf]
        need[("b", i)] -= x[i][j]
        need[("g", j)] -= x[i][j]
        left.discard((i, j))
    return x if all(v == 0 for v in need.values()) else None


def random_market(rng, nb, ng):
    while True:
        U = [[rng.choice([0, 1, 2, 3, 5, 8]) for _ in range(ng)] for _ in range(nb)]
        if all(any(r) for r in U) and all(any(U[i][j] for i in range(nb)) for j in range(ng)):
            return U, [rng.randint(1, 6) for _ in range(nb)]


class TestOrlinScaling(unittest.TestCase):
    def test_check_value(self):
        p, x = orlin_scaling([[2, 1], [1, 2]], [1, 1])
        self.assertEqual(p, [1, 1])
        self.assertEqual(x, [[1, 0], [0, 1]])

    def test_example(self):
        trace = []
        p, x = orlin_scaling([[1, 4, 3], [4, 2, 1], [1, 1, 2]], [1, 1, 3], trace)
        self.assertEqual(p, [Fraction(5, 4), Fraction(5, 4), Fraction(5, 2)])
        self.assertTrue(is_equilibrium([[1, 4, 3], [4, 2, 1], [1, 1, 2]], [1, 1, 3], p, x))
        self.assertEqual(trace[0][0], Fraction(1, 2))
        for (a, _, _), (b, _, _) in zip(trace, trace[1:]):
            self.assertEqual(b, a / 2)
        for delta, q, y in trace:
            # Delta-optimal at the end of each phase: every buyer has less than delta left, and
            # the money on each edge is a multiple of delta.
            for i in range(3):
                self.assertLess(Fraction([1, 1, 3][i]) - sum(y[i]), delta)
                self.assertTrue(all((v / delta).denominator == 1 for v in y[i]))
        # prices never go down
        for (_, q1, _), (_, q2, _) in zip(trace, trace[1:]):
            self.assertTrue(all(a <= b for a, b in zip(q1, q2)))

    def test_check_value_phases(self):
        trace = []
        orlin_scaling([[2, 1], [1, 2]], [1, 1], trace)
        self.assertEqual([d for d, _, _ in trace], [Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)])

    def test_identical_buyers(self):
        # The equilibrium allocation is not unique here; the prices are.
        p, x = orlin_scaling([[1, 1], [1, 1]], [1, 3])
        self.assertEqual(p, [2, 2])
        self.assertTrue(is_equilibrium([[1, 1], [1, 1]], [1, 3], p, x))

    def test_random_against_brute_force(self):
        rng = random.Random(9)
        for _ in range(40):
            nb, ng = rng.randint(1, 3), rng.randint(1, 3)
            U, e = random_market(rng, nb, ng)
            p, x = orlin_scaling(U, e)
            self.assertTrue(is_equilibrium(U, e, p, x))
            self.assertEqual(brute_force_prices(U, e), {tuple(p)})


if __name__ == "__main__":
    unittest.main()
