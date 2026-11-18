# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-operator-ordering/. The authors are listed in prov/X0F4M8.jsonl.

import random
import unittest
from fractions import Fraction

import dbrel
from greedy_operator_ordering import goo, leaves, plan_cost, plan_size


def linked(sel, A, B):
    return any((i in A and j in B) or (j in A and i in B) for i, j in sel)


def all_trees(sel, S, memo):
    """Every bushy tree over the set S whose joins all have an edge between their inputs."""
    if S in memo:
        return memo[S]
    if len(S) == 1:
        memo[S] = [next(iter(S))]
        return memo[S]
    out = []
    items = sorted(S)
    for mask in range(1, 1 << len(items)):
        A = frozenset(x for k, x in enumerate(items) if mask >> k & 1)
        B = S - A
        if B and linked(sel, A, B):
            for ta in all_trees(sel, A, memo):
                for tb in all_trees(sel, B, memo):
                    out.append((ta, tb))
    memo[S] = out
    return out


def random_query(rng, n, connected=True):
    sel = {}
    for i in range(1, n):
        if connected or rng.random() < 0.6:
            sel[(rng.randrange(i), i)] = Fraction(1, rng.choice([1, 2, 5, 10, 100]))
    for _ in range(rng.randint(0, n)):
        i, j = sorted(rng.sample(range(n), 2)) if n >= 2 else (0, 0)
        if i != j and (i, j) not in sel:
            sel[(i, j)] = Fraction(1, rng.choice([2, 10, 100]))
    card = [rng.choice([1, 10, 20, 100, 1000]) for _ in range(n)]
    return card, sel


class TestGOO(unittest.TestCase):
    def test_every_step_takes_the_smallest_join(self):
        rng = random.Random(1)
        for trial in range(300):
            n = rng.randint(1, 8)
            card, sel = random_query(rng, n, connected=trial % 3 != 0)
            cross = trial % 5 == 0
            trees = {frozenset([i]) for i in range(n)}

            def step(t1, t2, s):
                A, B = frozenset(leaves(t1)), frozenset(leaves(t2))
                self.assertIn(A, trees)
                self.assertIn(B, trees)
                self.assertNotEqual(A, B)
                cands = [(X, Y) for X in trees for Y in trees if X != Y]
                if not cross and any(linked(sel, X, Y) for X, Y in cands):
                    cands = [(X, Y) for X, Y in cands if linked(sel, X, Y)]
                    self.assertTrue(linked(sel, A, B))
                self.assertEqual(s, plan_size(card, sel, A | B))
                self.assertEqual(s, min(plan_size(card, sel, X | Y) for X, Y in cands))
                self.assertGreaterEqual(plan_size(card, sel, A), plan_size(card, sel, B))
                trees.difference_update((A, B))
                trees.add(A | B)

            cost, plan = goo(card, sel, cross_products=cross, on_step=step)
            self.assertEqual(len(trees), 1)
            self.assertEqual(sorted(leaves(plan)), list(range(n)))
            self.assertEqual(plan_cost(card, sel, plan), cost)

    def test_never_cheaper_than_the_optimum(self):
        rng = random.Random(2)
        worse = 0
        for _ in range(150):
            n = rng.randint(1, 5)
            card, sel = random_query(rng, n)
            cost, plan = goo(card, sel)
            trees = all_trees(sel, frozenset(range(n)), {})
            self.assertIn(plan, trees)
            best = min(plan_cost(card, sel, t) for t in trees)
            self.assertGreaterEqual(cost, best)
            if n <= 3:
                self.assertEqual(cost, best)
            worse += cost > best
        self.assertGreater(worse, 0)

    def test_counterexample(self):
        card = [20, 10, 1000, 20]
        sel = {(0, 1): Fraction(1, 5), (1, 2): Fraction(1, 100), (2, 3): Fraction(1, 100)}
        sizes = []
        cost, plan = goo(card, sel, on_step=lambda a, b, s: sizes.append(s))
        self.assertEqual(sizes, [40, 200, 80])
        self.assertEqual(cost, 320)
        self.assertEqual(plan, ((2, 3), (0, 1)))
        trees = all_trees(sel, frozenset(range(4)), {})
        best = min(trees, key=lambda t: plan_cost(card, sel, t))
        self.assertEqual(plan_cost(card, sel, best), 200)
        self.assertEqual(plan_cost(card, sel, (0, ((1, 2), 3))), 200)

    def test_cross_product_only_when_needed(self):
        card = [10, 10, 10, 10]
        sel = {(0, 1): Fraction(1, 2), (2, 3): Fraction(1, 2)}
        sizes = []
        cost, plan = goo(card, sel, on_step=lambda a, b, s: sizes.append(s))
        self.assertEqual(sizes, [50, 50, 2500])
        self.assertEqual(cost, 2600)
        card = [1, 1, 100]
        sel = {(0, 2): Fraction(1, 10), (1, 2): Fraction(1, 10)}
        self.assertEqual(goo(card, sel)[0], 10 + 1)
        self.assertEqual(goo(card, sel, cross_products=True), (Fraction(1 + 1), (2, (0, 1))))

    def test_plan_runs_and_gives_the_join(self):
        rng = random.Random(3)
        for _ in range(30):
            n = rng.randint(1, 5)
            card, sel = random_query(rng, n, connected=rng.random() < 0.8)
            attrs = {i: ["k%d" % i] + ["e%d_%d" % e for e in sel if i in e] for i in range(n)}
            db = {i: dbrel.random_relation(rng, attrs[i], rng.randint(0, 4), domain=2, null_rate=0.1)
                  for i in range(n)}
            _, plan = goo(card, sel)

            def run(p):
                if isinstance(p, int):
                    return db[p]
                return dbrel.natural_join(run(p[0]), run(p[1]))

            naive = db[0]
            for i in range(1, n):
                naive = dbrel.natural_join(naive, db[i])
            self.assertEqual(run(plan), naive)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            goo([], {})
        with self.assertRaises(ValueError):
            goo([1, 2], {(1, 1): Fraction(1, 2)})
        with self.assertRaises(ValueError):
            goo([1, 2], {(0, 2): Fraction(1, 2)})
        self.assertEqual(goo([7], {}), (0, 0))
        self.assertEqual(goo([3, 4], {(1, 0): Fraction(1, 2)}), (6, (1, 0)))


if __name__ == "__main__":
    unittest.main()
