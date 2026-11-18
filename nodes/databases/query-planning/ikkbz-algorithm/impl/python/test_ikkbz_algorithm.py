# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ikkbz-algorithm/. The authors are listed in prov/ZKFGDY.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import permutations

import dbrel
from ikkbz_algorithm import (Module, brute_force, cout, ikkbz, ikkbz_for_root, is_connected_order, join_size,
                             rooted_tree)


def random_tree(rng, n):
    perm = list(range(n))
    rng.shuffle(perm)
    sel = {}
    for i in range(1, n):
        a, b = perm[i], perm[rng.randrange(i)]
        sel[(min(a, b), max(a, b))] = Fraction(1, rng.choice([1, 2, 3, 5, 10, 20, 100]))
    card = [rng.randint(1, 100) for _ in range(n)]
    return card, sel


def seq_cost(T, seq):
    """C and T of a sequence of non-root relations, from the recurrence."""
    m = Module((), Fraction(1), Fraction(0))
    for v in seq:
        m = m.then(Module((v,), T[v], T[v]))
    return m


EXAMPLE_CARD = [100, 1000, 200, 50, 10]
EXAMPLE_SEL = {(0, 1): Fraction(1, 100), (0, 2): Fraction(1, 50), (2, 3): Fraction(1, 10), (2, 4): Fraction(1, 2)}


class TestIKKBZ(unittest.TestCase):
    def test_matches_brute_force(self):
        rng = random.Random(1)
        for _ in range(150):
            n = rng.randint(2, 7)
            card, sel = random_tree(rng, n)
            cost, order = ikkbz(card, sel)
            self.assertEqual(sorted(order), list(range(n)))
            self.assertTrue(is_connected_order(n, sel, order))
            self.assertEqual(cout(card, sel, order), cost)
            self.assertEqual(brute_force(card, sel)[0], cost)

    def test_each_root_is_optimal_for_that_root(self):
        rng = random.Random(2)
        for _ in range(60):
            n = rng.randint(2, 6)
            card, sel = random_tree(rng, n)
            for r in range(n):
                cost, order = ikkbz_for_root(n, card, sel, r)
                self.assertEqual(order[0], r)
                self.assertEqual(cout(card, sel, order), cost)
                best = min(cout(card, sel, (r,) + p) for p in permutations([v for v in range(n) if v != r])
                           if is_connected_order(n, sel, (r,) + p))
                self.assertEqual(cost, best)

    def test_cost_recurrence_equals_cout(self):
        rng = random.Random(3)
        for _ in range(100):
            n = rng.randint(2, 6)
            card, sel = random_tree(rng, n)
            r = rng.randrange(n)
            parent, _ = rooted_tree(n, sel, r)
            T = {v: sel[(min(v, parent[v]), max(v, parent[v]))] * card[v] for v in range(n) if v != r}
            for p in permutations([v for v in range(n) if v != r]):
                order = (r,) + p
                if is_connected_order(n, sel, order):
                    self.assertEqual(card[r] * seq_cost(T, p).C, cout(card, sel, order))
                    self.assertEqual(card[r] * seq_cost(T, p).T, join_size(card, sel, set(order)))

    def test_adjacent_sequence_interchange(self):
        rng = random.Random(4)
        for _ in range(500):
            T = {v: Fraction(rng.randint(1, 30), rng.randint(1, 30)) for v in range(6)}
            vs = list(range(6))
            rng.shuffle(vs)
            cuts = sorted(rng.sample(range(7), 3))
            U, A, B, V = vs[:cuts[0]], vs[cuts[0]:cuts[1]], vs[cuts[1]:cuts[2]], vs[cuts[2]:]
            if not A or not B:
                continue
            ma, mb, mu = seq_cost(T, A), seq_cost(T, B), seq_cost(T, U)
            diff = seq_cost(T, U + A + B + V).C - seq_cost(T, U + B + A + V).C
            self.assertEqual(diff, mu.T * ma.C * mb.C * (ma.rank() - mb.rank()))

    def test_worked_example(self):
        cost, order = ikkbz(EXAMPLE_CARD, EXAMPLE_SEL)
        self.assertEqual(cost, 112400)
        self.assertEqual(order, (0, 2, 3, 4, 1))
        per_root = [ikkbz_for_root(5, EXAMPLE_CARD, EXAMPLE_SEL, r) for r in range(5)]
        self.assertEqual([c for c, _ in per_root], [112400, 125000, 112400, 113000, 113000])
        self.assertEqual(per_root[3][1], (3, 2, 0, 4, 1))
        self.assertEqual(per_root[4][1], (4, 2, 0, 3, 1))

    def test_plan_runs_and_gives_the_join(self):
        rng = random.Random(5)
        for _ in range(40):
            n = rng.randint(2, 5)
            card, sel = random_tree(rng, n)
            _, order = ikkbz(card, sel)
            schema = {v: [] for v in range(n)}
            for (i, j) in sel:
                schema[i].append("k%d_%d" % (i, j))
                schema[j].append("k%d_%d" % (i, j))
            db = {v: dbrel.random_relation(rng, ["id%d" % v] + schema[v], rng.randint(0, 6), domain=3,
                                           null_rate=0.1) for v in range(n)}
            result = db[order[0]]
            for v in order[1:]:
                self.assertTrue(set(result.schema) & set(db[v].schema))
                result = dbrel.natural_join(result, db[v])
            naive = db[0]
            for v in range(1, n):
                naive = dbrel.natural_join(naive, db[v])
            self.assertEqual(result, naive)

    def test_rejects_cyclic_or_disconnected_graphs(self):
        with self.assertRaises(ValueError):
            ikkbz([10, 10, 10], {(0, 1): Fraction(1, 2), (1, 2): Fraction(1, 2), (0, 2): Fraction(1, 2)})
        with self.assertRaises(ValueError):
            ikkbz([10, 10, 10, 10], {(0, 1): Fraction(1, 2), (2, 3): Fraction(1, 2)})

    def test_small_inputs(self):
        self.assertEqual(ikkbz([7], {}), (0, (0,)))
        self.assertEqual(ikkbz([10, 20], {(0, 1): Fraction(1, 10)}), (Fraction(20), (0, 1)))


if __name__ == "__main__":
    unittest.main()
