# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jain-vazirani-steiner-cost-sharing/. The authors are listed in prov/F0QV3E.jsonl.
"""Tests for jain_vazirani_steiner_cost_sharing: the worked example, edge cases, and random
graphs checked against an independent simulation of the directed primal-dual algorithm, the
MST of the metric closure, a brute-force optimal Steiner tree, and cross-monotonicity."""

import random
import unittest
from fractions import Fraction as F
from itertools import combinations

from jain_vazirani_steiner_cost_sharing import jv_cost_shares, metric_closure, mst_cost

# Root 0, terminals 1 (a), 2 (b), 3 (c), Steiner vertex 4 (s).
EXAMPLE = [(0, 4, 4), (4, 1, 1), (4, 2, 1), (4, 3, 2), (0, 3, 5)]


def primal_dual_oracle(d, root, terminals):
    """Event-by-event simulation of the primal-dual algorithm on the bidirected closure.

    Each arc (u, v) has a load: the sum of the duals of the sets that contain v but not u.
    An arc is tight when its load equals d(u, v). The active sets are the strongly connected
    components of the tight arcs that do not contain the root and have no tight arc entering
    them. Each active set raises its dual at rate 1 and splits it equally among its members."""
    pts = [root] + sorted(terminals)
    arcs = [(u, v) for u in pts for v in pts if u != v]
    load = {a: F(0) for a in arcs}
    tight = {a for a in arcs if d[a[0]][a[1]] == 0}
    share = {i: F(0) for i in terminals}
    while True:
        reach = {u: {u} for u in pts}
        changed = True
        while changed:
            changed = False
            for u, v in tight:
                for x in pts:
                    if u in reach[x] and not reach[v] <= reach[x]:
                        reach[x] |= reach[v]
                        changed = True
        sccs = {frozenset(y for y in reach[x] if x in reach[y]) for x in pts}
        active = [C for C in sccs if root not in C
                  and not any(u not in C and v in C for u, v in tight)]
        if not active:
            return share
        growing = [(u, v) for C in active for (u, v) in arcs if v in C and u not in C]
        dt = min(d[u][v] - load[(u, v)] for u, v in growing)
        for C in active:
            for i in C:
                share[i] += dt / len(C)
        for a in growing:
            load[a] += dt
            if load[a] == d[a[0]][a[1]]:
                tight.add(a)


def steiner_opt(d, n, root, terminals):
    """Optimal Steiner tree cost: the best MST over terminals, root and a set of other vertices."""
    others = [v for v in range(n) if v != root and v not in terminals]
    best = None
    for k in range(len(others) + 1):
        for extra in combinations(others, k):
            c = mst_cost(d, [root] + list(terminals) + list(extra))
            if best is None or c < best:
                best = c
    return best


def random_graph(rng, n):
    edges = []
    for v in range(1, n):
        edges.append((rng.randrange(v), v, rng.randint(1, 9)))
    for u, v in combinations(range(n), 2):
        if rng.random() < 0.35:
            edges.append((u, v, rng.randint(1, 9)))
    return edges


class TestJainVazirani(unittest.TestCase):
    def test_worked_example(self):
        shares = jv_cost_shares(5, EXAMPLE, 0, [1, 2, 3])
        self.assertEqual(shares, {1: F(19, 6), 2: F(19, 6), 3: F(11, 3)})
        d = metric_closure(5, EXAMPLE)
        self.assertEqual(sum(shares.values()), 10)
        self.assertEqual(mst_cost(d, [0, 1, 2, 3]), 10)
        self.assertEqual(steiner_opt(d, 5, 0, [1, 2, 3]), 8)
        self.assertEqual(jv_cost_shares(5, EXAMPLE, 0, [1, 2]), {1: F(7, 2), 2: F(7, 2)})
        self.assertEqual(jv_cost_shares(5, EXAMPLE, 0, [1, 3]), {1: F(4), 3: F(4)})
        for i in (1, 2, 3):
            self.assertEqual(jv_cost_shares(5, EXAMPLE, 0, [i]), {i: F(5)})

    def test_edge_cases(self):
        self.assertEqual(jv_cost_shares(1, [], 0, []), {})
        self.assertEqual(jv_cost_shares(2, [(0, 1, 3)], 0, [1, 1]), {1: F(3)})
        self.assertEqual(jv_cost_shares(3, [(0, 1, 0), (1, 2, 0)], 0, [1, 2]), {1: 0, 2: 0})
        with self.assertRaises(ValueError):
            jv_cost_shares(2, [(0, 1, 3)], 0, [0])
        with self.assertRaises(ValueError):
            jv_cost_shares(3, [(0, 1, 3)], 0, [2])
        with self.assertRaises(ValueError):
            jv_cost_shares(2, [(0, 1, -1)], 0, [1])
        with self.assertRaises(ValueError):
            jv_cost_shares(2, [(0, 1, 1)], 0, [5])

    def test_random_against_oracle_and_bounds(self):
        rng = random.Random(3)
        for _ in range(250):
            n = rng.randint(2, 7)
            edges = random_graph(rng, n)
            d = metric_closure(n, edges)
            root = rng.randrange(n)
            others = [v for v in range(n) if v != root]
            terms = sorted(rng.sample(others, rng.randint(1, len(others))))
            shares = jv_cost_shares(n, edges, root, terms)
            self.assertEqual(shares, primal_dual_oracle(d, root, terms))
            total = sum(shares.values())
            self.assertEqual(total, mst_cost(d, [root] + terms))
            opt = steiner_opt(d, n, root, terms)
            self.assertLessEqual(opt, total)
            self.assertLessEqual(total, 2 * opt)

    def test_cross_monotonic(self):
        rng = random.Random(4)
        for _ in range(60):
            n = rng.randint(3, 7)
            edges = random_graph(rng, n)
            terms = list(range(1, n))
            full = {}
            for k in range(1, len(terms) + 1):
                for S in combinations(terms, k):
                    full[S] = jv_cost_shares(n, edges, 0, S)
            for S, sh in full.items():
                for k in range(1, len(S)):
                    for T in combinations(S, k):
                        for i in T:
                            self.assertGreaterEqual(full[T][i], sh[i])

    def test_fractional_costs(self):
        edges = [(0, 1, F(1, 2)), (1, 2, F(1, 3)), (0, 2, F(5, 6))]
        shares = jv_cost_shares(3, edges, 0, [1, 2])
        self.assertEqual(sum(shares.values()), F(5, 6))
        self.assertEqual(shares, {1: F(1, 3) + F(1, 12), 2: F(1, 3) + F(1, 12)})


if __name__ == "__main__":
    unittest.main()
