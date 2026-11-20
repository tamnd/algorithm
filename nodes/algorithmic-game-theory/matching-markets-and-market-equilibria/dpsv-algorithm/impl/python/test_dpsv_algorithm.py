# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpsv-algorithm/. The authors are listed in prov/MZRKQA.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations

from dpsv_algorithm import dpsv

# The example of the page: 3 buyers and 3 goods.
EXAMPLE_U = [[1, 4, 3], [4, 2, 1], [1, 1, 2]]
EXAMPLE_E = [1, 1, 3]


def is_equilibrium(u, e, p, x):
    """Exact check: every buyer spends all her money, only on goods of maximum bang per buck,
    and every good is sold out (all prices are positive)."""
    n, m = len(u), len(u[0])
    if any(q <= 0 for q in p):
        return False
    for i in range(n):
        best = max(Fraction(u[i][j]) / p[j] for j in range(m))
        if sum(x[i]) != e[i]:
            return False
        for j in range(m):
            if x[i][j] < 0 or (x[i][j] > 0 and Fraction(u[i][j]) / p[j] != best):
                return False
    return all(sum(x[i][j] for i in range(n)) == p[j] for j in range(m))


def brute_force_prices(u, e):
    """All equilibrium price vectors, by trying every set of spending edges as the support:
    the prices on a connected support are fixed by the utility ratios and by the budgets."""
    n, m = len(u), len(u[0])
    all_edges = [(i, j) for i in range(n) for j in range(m) if u[i][j] > 0]
    found = set()
    for k in range(1, len(all_edges) + 1):
        for H in combinations(all_edges, k):
            p = prices_from_support(u, e, H)
            if p is None:
                continue
            x = support_flow(u, e, p, H)
            if x is not None and is_equilibrium(u, e, p, x):
                found.add(tuple(p))
    return found


def prices_from_support(u, e, H):
    n, m = len(u), len(u[0])
    rel = {}  # node -> price (goods) or bang per buck (buyers), up to a factor per component
    comps = []
    for start in range(m):
        if ("g", start) in rel:
            continue
        rel[("g", start)] = Fraction(1)
        stack, comp = [("g", start)], [("g", start)]
        while stack:
            kind, a = stack.pop()
            for i, j in H:
                if kind == "g" and j == a:
                    nxt, val = ("b", i), Fraction(u[i][j]) / rel[("g", j)]
                elif kind == "b" and i == a:
                    nxt, val = ("g", j), Fraction(u[i][j]) / rel[("b", i)]
                else:
                    continue
                if nxt in rel:
                    if rel[nxt] != val:
                        return None
                else:
                    rel[nxt] = val
                    stack.append(nxt)
                    comp.append(nxt)
        comps.append(comp)
    if any(("b", i) not in rel for i in range(n)):
        return None
    p = [None] * m
    for comp in comps:
        money = sum(Fraction(e[a]) for kind, a in comp if kind == "b")
        if money == 0:
            return None
        scale = money / sum(rel[(kind, a)] for kind, a in comp if kind == "g")
        for kind, a in comp:
            if kind == "g":
                p[a] = rel[(kind, a)] * scale
    return p


def support_flow(u, e, p, H):
    """Spend along the support H by solving the flow on a forest (peel leaves); None if H has a
    cycle or the flow would be negative."""
    n, m = len(u), len(u[0])
    if len(H) > n + m - 1:
        return None
    x = [[Fraction(0)] * m for _ in range(n)]
    left = set(H)
    need = {("b", i): Fraction(e[i]) for i in range(n)}
    need.update({("g", j): p[j] for j in range(m)})
    while left:
        deg = {}
        for i, j in left:
            deg[("b", i)] = deg.get(("b", i), 0) + 1
            deg[("g", j)] = deg.get(("g", j), 0) + 1
        leaf = next((v for v, d in deg.items() if d == 1), None)
        if leaf is None:
            return None
        (i, j) = next(ed for ed in left if ("b", ed[0]) == leaf or ("g", ed[1]) == leaf)
        amount = need[leaf]
        if amount < 0:
            return None
        x[i][j] = amount
        need[("b", i)] -= amount
        need[("g", j)] -= amount
        left.discard((i, j))
    if any(v != 0 for v in need.values()):
        return None
    return x


def random_market(rng, n, m):
    while True:
        u = [[rng.choice([0, 1, 2, 3, 4, 5]) for _ in range(m)] for _ in range(n)]
        if all(any(row) for row in u) and all(any(u[i][j] for i in range(n)) for j in range(m)):
            return u, [rng.randint(1, 4) for _ in range(n)]


class TestDPSV(unittest.TestCase):
    def test_check_value(self):
        p, x = dpsv([[2, 1], [1, 2]], [1, 1])
        self.assertEqual(p, [1, 1])
        self.assertEqual(x, [[1, 0], [0, 1]])

    def test_example(self):
        trace = []
        p, x = dpsv(EXAMPLE_U, EXAMPLE_E, trace)
        self.assertEqual(p, [Fraction(5, 4), Fraction(5, 4), Fraction(5, 2)])
        self.assertTrue(is_equilibrium(EXAMPLE_U, EXAMPLE_E, p, x))
        self.assertEqual(x, [[0, 1, 0], [1, 0, 0], [Fraction(1, 4), Fraction(1, 4), Fraction(5, 2)]])
        self.assertEqual(trace, [(Fraction(3), "freeze", [0, 1]), (Fraction(2), "unfreeze", [0, 1]),
                                 (Fraction(5, 4), "freeze", [0, 1, 2])])

    def test_one_buyer(self):
        # A single buyer must find every good a best buy, so prices are proportional to utilities.
        p, x = dpsv([[1, 3, 2]], [6])
        self.assertEqual(p, [1, 3, 2])
        self.assertEqual(x, [[1, 3, 2]])

    def test_random_against_brute_force(self):
        rng = random.Random(7)
        for _ in range(40):
            n, m = rng.randint(1, 3), rng.randint(1, 3)
            u, e = random_market(rng, n, m)
            p, x = dpsv(u, e)
            self.assertTrue(is_equilibrium(u, e, p, x))
            self.assertEqual(brute_force_prices(u, e), {tuple(p)})

    def test_prices_never_fall(self):
        rng = random.Random(11)
        for _ in range(30):
            u, e = random_market(rng, 3, 3)
            trace = []
            dpsv(u, e, trace)
            self.assertTrue(all(f >= 1 for f, _, _ in trace))


if __name__ == "__main__":
    unittest.main()
