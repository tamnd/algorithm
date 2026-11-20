# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kidney-exchange-cycle-formulation/. The authors are listed in prov/HATF0Q.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import permutations

from kidney_exchange_cycle_formulation import kidney_exchange, short_cycles


def cycles_by_permutations(n, arcs, L):
    """Reference cycle list: try every sequence of distinct vertices."""
    A = set(arcs)
    out = set()
    for k in range(2, L + 1):
        for seq in permutations(range(n), k):
            if seq[0] == min(seq) and all((seq[t], seq[(t + 1) % k]) in A for t in range(k)):
                out.add(seq)
    return out


def brute_force(n, arcs, L, w=None):
    """Best packing of disjoint short cycles by trying every subset of compatible cycles."""
    w = {a: 1 for a in arcs} if w is None else w
    cyc = sorted(cycles_by_permutations(n, arcs, L))
    wt = [sum(w[(c[k], c[(k + 1) % len(c)])] for k in range(len(c))) for c in cyc]
    best = 0

    def rec(k, used, val):
        nonlocal best
        best = max(best, val)
        for t in range(k, len(cyc)):
            if not used.intersection(cyc[t]):
                rec(t + 1, used | set(cyc[t]), val + wt[t])

    rec(0, set(), 0)
    return best


def check_solution(test, n, arcs, L, w, value, cycles):
    w = {a: 1 for a in arcs} if w is None else w
    A = set(arcs)
    seen = set()
    total = 0
    for c in cycles:
        test.assertTrue(2 <= len(c) <= L)
        test.assertFalse(seen.intersection(c))
        seen.update(c)
        for k in range(len(c)):
            a = (c[k], c[(k + 1) % len(c)])
            test.assertIn(a, A)
            total += w[a]
    test.assertEqual(total, value)


class TestKidneyExchange(unittest.TestCase):
    def test_page_examples(self):
        arcs = [(0, 1), (1, 2), (2, 0), (1, 0), (2, 3), (3, 2), (3, 4), (4, 3)]
        self.assertEqual(kidney_exchange(5, arcs, 2)[:2], (4, [(0, 1), (2, 3)]))
        self.assertEqual(kidney_exchange(5, arcs, 3)[:2], (5, [(0, 1, 2), (3, 4)]))
        # three mutual pairs: the root LP is 3 with all 2-cycles at 1/2, the optimum is 2
        tri = [(0, 1), (1, 0), (1, 2), (2, 1), (2, 0), (0, 2)]
        value, cyc, stats = kidney_exchange(3, tri, 2)
        self.assertEqual((value, stats["root_lp"], stats["nodes"]), (2, Fraction(3), 3))
        self.assertEqual(len(cyc), 1)
        self.assertEqual(kidney_exchange(3, tri, 3)[:2], (3, [(0, 1, 2)]))

    def test_edge_cases(self):
        self.assertEqual(kidney_exchange(0, [], 3)[:2], (0, []))
        self.assertEqual(kidney_exchange(1, [], 3)[:2], (0, []))
        self.assertEqual(kidney_exchange(2, [(0, 1)], 3)[:2], (0, []))
        self.assertEqual(kidney_exchange(2, [(0, 1), (1, 0)], 2)[:2], (2, [(0, 1)]))
        # a 4-cycle is not allowed with L = 3
        ring = [(0, 1), (1, 2), (2, 3), (3, 0)]
        self.assertEqual(kidney_exchange(4, ring, 3)[0], 0)
        self.assertEqual(kidney_exchange(4, ring, 4)[0], 4)

    def test_cycle_enumeration(self):
        rng = random.Random(2)
        for _ in range(40):
            n = rng.randint(1, 6)
            arcs = [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < 0.4]
            succ = [[] for _ in range(n)]
            for i, j in arcs:
                succ[i].append(j)
            for L in (2, 3, 4):
                got = short_cycles(n, succ, L)
                self.assertEqual(len(got), len(set(got)))
                self.assertEqual(set(got), cycles_by_permutations(n, arcs, L))

    def test_against_brute_force(self):
        rng = random.Random(7)
        for _ in range(120):
            n = rng.randint(1, 8)
            p = rng.choice([0.2, 0.35, 0.5])
            arcs = [(i, j) for i in range(n) for j in range(n) if i != j and rng.random() < p]
            L = rng.choice([2, 3, 4])
            w = {a: rng.randint(1, 5) for a in arcs} if rng.random() < 0.5 else None
            value, cycles, stats = kidney_exchange(n, arcs, L, w)
            self.assertEqual(value, brute_force(n, arcs, L, w))
            check_solution(self, n, arcs, L, w, value, cycles)
            self.assertGreaterEqual(stats["root_lp"], value)  # the LP is an upper bound


if __name__ == "__main__":
    unittest.main()
