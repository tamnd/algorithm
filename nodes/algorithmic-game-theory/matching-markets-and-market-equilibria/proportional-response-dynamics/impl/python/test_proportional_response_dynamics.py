# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proportional-response-dynamics/. The authors are listed in prov/M8R35N.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations

from proportional_response_dynamics import kl, prices, proportional_response, shmyrev

TOL = 1e-9  # slack for floating point rounding in the exact inequalities


def equilibrium_spending(u, e):
    """An exact equilibrium of the market, as money spent b[i][j], found by trying every forest of
    spending edges. The forest fixes the prices: equal bang per buck along each buyer's edges, and
    on each connected part the prices add up to the budgets."""
    n, m = len(u), len(u[0])
    all_edges = [(i, j) for i in range(n) for j in range(m) if u[i][j] > 0]
    for k in range(1, min(len(all_edges), n + m - 1) + 1):
        for H in combinations(all_edges, k):
            p = forest_prices(u, e, H)
            if p is None:
                continue
            b = forest_flow(n, m, e, p, H)
            if b is not None and is_equilibrium(u, e, p, b):
                return p, b
    raise AssertionError("no equilibrium found")


def forest_prices(u, e, H):
    n, m = len(u), len(u[0])
    nbr = {}
    for i, j in H:
        nbr.setdefault(("b", i), []).append(("g", j))
        nbr.setdefault(("g", j), []).append(("b", i))
    if len(nbr) != n + m:
        return None
    rel, p = {}, [None] * m
    for j0 in range(m):
        if ("g", j0) in rel:
            continue
        rel[("g", j0)] = Fraction(1)
        comp, stack = [("g", j0)], [("g", j0)]
        while stack:
            a = stack.pop()
            for c in nbr[a]:
                i, j = (a[1], c[1]) if a[0] == "b" else (c[1], a[1])
                val = Fraction(u[i][j]) / rel[a]
                if c not in rel:
                    rel[c] = val
                    comp.append(c)
                    stack.append(c)
                elif rel[c] != val:
                    return None
        money = sum(e[a[1]] for a in comp if a[0] == "b")
        scale = money / sum(rel[a] for a in comp if a[0] == "g")
        for a in comp:
            if a[0] == "g":
                p[a[1]] = rel[a] * scale
    return p


def forest_flow(n, m, e, p, H):
    left = set(H)
    need = {("b", i): Fraction(e[i]) for i in range(n)}
    need.update({("g", j): p[j] for j in range(m)})
    b = [[Fraction(0)] * m for _ in range(n)]
    while left:
        deg = {}
        for i, j in left:
            deg[("b", i)] = deg.get(("b", i), 0) + 1
            deg[("g", j)] = deg.get(("g", j), 0) + 1
        leaf = next((v for v, d in deg.items() if d == 1), None)
        if leaf is None:
            return None
        i, j = next(ed for ed in left if ("b", ed[0]) == leaf or ("g", ed[1]) == leaf)
        amount = need[leaf]
        if amount < 0:
            return None
        b[i][j] = amount
        need[("b", i)] -= amount
        need[("g", j)] -= amount
        left.discard((i, j))
    return b if all(v == 0 for v in need.values()) else None


def is_equilibrium(u, e, p, b):
    n, m = len(u), len(u[0])
    for i in range(n):
        best = max(Fraction(u[i][j]) / p[j] for j in range(m))
        if sum(b[i]) != e[i]:
            return False
        if any(b[i][j] > 0 and Fraction(u[i][j]) / p[j] != best for j in range(m)):
            return False
    return all(sum(b[i][j] for i in range(n)) == p[j] for j in range(m))


def random_market(rng, n, m):
    while True:
        u = [[rng.choice([0, 1, 2, 3, 4]) for _ in range(m)] for _ in range(n)]
        if all(any(r) for r in u) and all(any(u[i][j] for i in range(n)) for j in range(m)):
            return u, [rng.randint(1, 3) for _ in range(n)]


class TestProportionalResponse(unittest.TestCase):
    def test_check_value(self):
        history = proportional_response([[2, 1], [1, 2]], [1, 1], 60)
        for t, b in enumerate(history[:20]):
            # From an even split, buyer 1 bids 2^t / (2^t + 1) on good 1 in round t.
            self.assertAlmostEqual(b[0][0], 2 ** t / (2 ** t + 1), delta=1e-12)
            self.assertAlmostEqual(prices(b)[0], 1.0, delta=1e-12)
        self.assertAlmostEqual(history[-1][0][0], 1.0, delta=1e-12)

    def test_example(self):
        # The example of the page: the equilibrium prices are (1, 2).
        history = proportional_response([[1, 1], [1, 3]], [1, 2], 50)
        expected = {0: (1.5, 1.5), 1: (1.0, 2.0), 2: (34 / 33, 65 / 33)}
        for t, (p1, p2) in expected.items():
            self.assertAlmostEqual(prices(history[t])[0], p1, delta=1e-12)
            self.assertAlmostEqual(prices(history[t])[1], p2, delta=1e-12)
        self.assertAlmostEqual(history[2][0][0], 2 / 3, delta=1e-12)
        self.assertAlmostEqual(history[2][1][1], 18 / 11, delta=1e-12)
        p = prices(history[-1])
        self.assertAlmostEqual(p[0], 1.0, delta=1e-4)
        self.assertAlmostEqual(p[1], 2.0, delta=1e-4)

    def test_degenerate_market_is_slow(self):
        # At the prices (2, 1), buyer 1 is indifferent between the goods but must not buy good 2.
        history = proportional_response([[2, 1], [1, 2]], [2, 1], 1000)
        p = prices(history[-1])
        self.assertGreater(abs(p[0] - 2.0), 1e-4)
        self.assertLess(abs(p[0] - 2.0), 1e-2)

    def test_budgets_and_bound(self):
        rng = random.Random(1)
        for _ in range(25):
            n, m = rng.randint(1, 3), rng.randint(1, 3)
            u, e = random_market(rng, n, m)
            p_star, b_star = equilibrium_spending(u, e)
            b_star = [[float(v) for v in row] for row in b_star]
            phi_star = shmyrev(u, b_star)
            history = proportional_response(u, [float(v) for v in e], 300)
            start = kl(b_star, history[0])
            last = None
            for t, b in enumerate(history):
                for i in range(n):
                    self.assertAlmostEqual(sum(b[i]), e[i], delta=1e-9)
                phi = shmyrev(u, b)
                self.assertGreaterEqual(phi, phi_star - TOL)
                if last is not None:
                    self.assertLessEqual(phi, last + TOL)
                if t > 0:
                    self.assertLessEqual(phi - phi_star, start / t + TOL)
                last = phi

    def test_prices_converge(self):
        rng = random.Random(2)
        for _ in range(6):
            u, e = random_market(rng, 3, 3)
            p_star, _ = equilibrium_spending(u, e)
            history = proportional_response(u, [float(v) for v in e], 1500)
            p = prices(history[-1])
            for j in range(3):
                self.assertAlmostEqual(p[j], float(p_star[j]), delta=2e-2)


if __name__ == "__main__":
    unittest.main()
