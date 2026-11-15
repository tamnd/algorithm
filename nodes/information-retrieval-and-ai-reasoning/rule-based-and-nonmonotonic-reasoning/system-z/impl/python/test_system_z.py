# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/system-z/. The authors are listed in prov/8532GG.jsonl.

import random
import unittest
from itertools import product

from system_z import (
    FALSE,
    INF,
    TRUE,
    conj,
    disj,
    entails,
    evaluate,
    kappa,
    neg,
    partition,
    rank_world,
    satisfiable,
    var,
    z_ranks,
)

a, b, c, d = var("a"), var("b"), var("c"), var("d")


def worlds(names):
    return [dict(zip(names, v)) for v in product([False, True], repeat=len(names))]


def holds(rule, w):
    return not evaluate(rule[0], w) or evaluate(rule[1], w)


def exceptional_bf(alpha, rules, ws):
    """Lehmann and Magidor: alpha is exceptional for C when no world satisfies alpha and every material counterpart in C."""
    return not any(evaluate(alpha, w) and all(holds(r, w) for r in rules) for w in ws)


def partition_bf(rules, ws):
    rest, layers = list(range(len(rules))), []
    while rest:
        layer = [
            i for i in rest
            if any(evaluate(rules[i][0], w) and evaluate(rules[i][1], w) and all(holds(rules[j], w) for j in rest) for w in ws)
        ]
        if not layer:
            return layers, rest
        layers.append(layer)
        rest = [i for i in rest if i not in layer]
    return layers, []


def world_rank_bf(rules, split, w):
    layers, rest = split
    z = {i: k for k, layer in enumerate(layers) for i in layer}
    bad = [i for i, r in enumerate(rules) if not holds(r, w)]
    if any(i in rest for i in bad):
        return INF
    return 1 + max(z[i] for i in bad) if bad else 0


def kappa_bf(rules, split, phi, ws):
    return min((world_rank_bf(rules, split, w) for w in ws if evaluate(phi, w)), default=INF)


def rational_closure_bf(rules, alpha, beta, ws):
    """The decision procedure of Lehmann and Magidor (1992, Section 5.8), with exceptionality decided by enumeration."""
    cur = list(rules)
    while exceptional_bf(alpha, cur, ws):
        nxt = [r for r in cur if exceptional_bf(r[0], cur, ws)]
        if nxt == cur:
            break
        cur = nxt
    return exceptional_bf(conj(alpha, neg(beta)), cur, ws)


def random_formula(rng, names, depth):
    if depth == 0 or rng.random() < 0.3:
        x = var(rng.choice(names))
        r = rng.random()
        if r < 0.05:
            return TRUE
        if r < 0.08:
            return FALSE
        return neg(x) if rng.random() < 0.4 else x
    op = rng.choice(["and", "or", "not"])
    if op == "not":
        return neg(random_formula(rng, names, depth - 1))
    kids = [random_formula(rng, names, depth - 1) for _ in range(rng.randint(2, 3))]
    return conj(*kids) if op == "and" else disj(*kids)


def random_rules(rng, names):
    return [
        (random_formula(rng, names, rng.randint(0, 2)), random_formula(rng, names, rng.randint(0, 2)))
        for _ in range(rng.randint(1, 5))
    ]


class TestOracle(unittest.TestCase):
    def test_satisfiable_matches_truth_tables(self):
        rng = random.Random(2)
        names = ["a", "b", "c", "d"]
        ws = worlds(names)
        for _ in range(800):
            f = random_formula(rng, names, 3)
            self.assertEqual(satisfiable(f), any(evaluate(f, w) for w in ws), f)
        self.assertTrue(satisfiable(TRUE))
        self.assertFalse(satisfiable(FALSE))
        self.assertFalse(satisfiable(conj(a, neg(a))))


class TestAgainstBruteForce(unittest.TestCase):
    def test_partition_ranks_and_rational_closure(self):
        rng = random.Random(1990)
        for _ in range(150):
            names = ["a", "b", "c", "d"][: rng.randint(1, 4)]
            ws = worlds(names)
            rules = random_rules(rng, names)
            split = partition(rules)
            self.assertEqual(split, partition_bf(rules, ws), rules)
            for w in ws:
                self.assertEqual(rank_world(w, rules, split), world_rank_bf(rules, split, w))
            for _ in range(6):
                alpha = random_formula(rng, names, 2)
                beta = random_formula(rng, names, 2)
                self.assertEqual(kappa(alpha, rules, split), kappa_bf(rules, split, alpha, ws))
                self.assertEqual(
                    entails(rules, alpha, beta, split),
                    rational_closure_bf(rules, alpha, beta, ws),
                    (rules, alpha, beta),
                )
            for rule in rules:  # every rule is entailed by its own set
                self.assertTrue(entails(rules, rule[0], rule[1], split))

    def test_least_admissible_ranking(self):
        # Over two atoms, try every ranking with values 0 to 3 that gives some world rank 0.
        rng = random.Random(1992)
        names = ["a", "b"]
        ws = worlds(names)
        all_rankings = [r for r in product(range(4), repeat=len(ws)) if 0 in r]

        def rank_of(ranking, phi):
            return min((ranking[k] for k, w in enumerate(ws) if evaluate(phi, w)), default=INF)

        def admissible(ranking, rules):
            return all(rank_of(ranking, conj(x, y)) < rank_of(ranking, conj(x, neg(y))) for x, y in rules)

        checked = 0
        while checked < 25:
            rules = random_rules(rng, names)
            split = partition(rules)
            if split[1]:
                self.assertFalse(any(admissible(r, rules) for r in all_rankings))
                continue
            checked += 1
            kz = tuple(rank_world(w, rules, split) for w in ws)
            self.assertTrue(admissible(kz, rules))
            for r in all_rankings:
                if admissible(r, rules):
                    self.assertTrue(all(x <= y for x, y in zip(kz, r)), (rules, r))


class TestExamples(unittest.TestCase):
    def setUp(self):
        self.bird, self.fly, self.penguin, self.wings = var("b"), var("f"), var("p"), var("w")

    def test_penguin(self):
        b_, f_, p_ = self.bird, self.fly, self.penguin
        rules = [(b_, f_), (p_, b_), (p_, neg(f_))]
        self.assertEqual(partition(rules), ([[0], [1, 2]], []))
        self.assertEqual(z_ranks(rules), {0: 0, 1: 1, 2: 1})
        self.assertTrue(entails(rules, b_, f_))
        self.assertTrue(entails(rules, p_, neg(f_)))
        self.assertTrue(entails(rules, p_, b_))
        self.assertTrue(entails(rules, conj(b_, neg(p_)), f_))
        self.assertFalse(entails(rules, p_, f_))
        self.assertEqual(kappa(p_, rules), 1)
        self.assertEqual(kappa(b_, rules), 0)
        self.assertTrue(entails(rules, b_, neg(p_)))  # birds are normally not penguins

    def test_drowning(self):
        b_, f_, p_, w_ = self.bird, self.fly, self.penguin, self.wings
        rules = [(b_, f_), (p_, b_), (p_, neg(f_)), (b_, w_)]
        self.assertEqual(partition(rules)[0], [[0, 3], [1, 2]])
        self.assertTrue(entails(rules, b_, w_))
        self.assertFalse(entails(rules, p_, w_))
        self.assertFalse(entails(rules, p_, neg(w_)))

    def test_nixon(self):
        q, r, p = var("q"), var("r"), var("pacifist")
        rules = [(q, p), (r, neg(p))]
        self.assertEqual(partition(rules), ([[0, 1]], []))
        self.assertFalse(entails(rules, conj(q, r), p))
        self.assertFalse(entails(rules, conj(q, r), neg(p)))
        self.assertTrue(entails(rules, q, p))

    def test_irrelevance(self):
        rules = [(a, b)]
        self.assertTrue(entails(rules, conj(a, c), b))

    def test_inconsistent_sets(self):
        for rules in ([(a, b), (a, neg(b))], [(TRUE, a), (TRUE, neg(a))], [(a, FALSE)]):
            layers, rest = partition(rules)
            self.assertTrue(rest)
            self.assertEqual(kappa(a, rules), INF)
            self.assertTrue(entails(rules, a, c))
        self.assertEqual(partition([(a, b), (a, neg(b)), (c, d)]), ([[2]], [0, 1]))

    def test_empty_set(self):
        self.assertEqual(partition([]), ([], []))
        self.assertTrue(entails([], a, a))
        self.assertFalse(entails([], a, b))
        self.assertTrue(entails([], FALSE, b))


if __name__ == "__main__":
    unittest.main()
