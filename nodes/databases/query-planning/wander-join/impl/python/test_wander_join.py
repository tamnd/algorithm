# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wander-join/. The authors are listed in prov/SRQFRM.jsonl.

import itertools
import math
import unittest
from fractions import Fraction
from random import Random

from wander_join import WalkPlan, choose_plan, wander_join


def brute_force_sum(relations, value, predicates=None):
    """SUM(value) over the natural join, by nested loops over all relations."""
    predicates = predicates or {}
    names = sorted(relations)
    total = Fraction(0)
    for combo in itertools.product(*(relations[n] for n in names)):
        joined = {}
        good = True
        for name, row in zip(names, combo):
            if name in predicates and not predicates[name](row):
                good = False
                break
            for a, x in row.items():
                if a in joined and joined[a] != x:
                    good = False
                    break
                joined[a] = x
            if not good:
                break
        if good:
            total += Fraction(value(joined))
    return total


def valid_orders(relations):
    attrs = {n: set(rows[0]) for n, rows in relations.items()}
    for order in itertools.permutations(sorted(relations)):
        if all(any(attrs[order[j]] & attrs[order[i]] for j in range(i)) for i in range(1, len(order))):
            yield order


def page_example():
    R1 = [{"A": "a1", "B": "b1"}, {"A": "a2", "B": "b1"}, {"A": "a3", "B": "b2"}]
    R2 = [{"B": "b1", "C": "c1"}, {"B": "b1", "C": "c2"}, {"B": "b2", "C": "c3"}]
    R3 = [{"C": "c1", "D": 5}, {"C": "c2", "D": 1}, {"C": "c2", "D": 3}]
    return {"R1": R1, "R2": R2, "R3": R3}


def random_instance(rng, shape):
    dom = rng.randint(2, 4)

    def rel(schema, n):
        return [{a: rng.randrange(dom) for a in schema} | {"w": rng.randint(1, 9)} for _ in range(n)]

    if shape == "chain":
        rels = {"R": rel("ab", 5), "S": rel("bc", 5), "T": rel("cd", 5)}
    elif shape == "star":
        rels = {"R": rel("ab", 5), "S": rel("bc", 4), "T": rel("bd", 4), "U": rel("de", 3)}
    else:
        rels = {"R": rel("ab", 5), "S": rel("bc", 5), "T": rel("ca", 5)}
    # the weight column w is private to each relation
    for name, rows in rels.items():
        for row in rows:
            row["w_" + name] = row.pop("w")
    return rels


def weight_product(joined):
    return math.prod(x for a, x in joined.items() if a.startswith("w_"))


class TestExample(unittest.TestCase):
    def test_walks_of_the_page(self):
        rels = page_example()
        D = lambda j: j["D"]
        self.assertEqual(brute_force_sum(rels, D), 18)
        plan = WalkPlan(rels, ["R1", "R2", "R3"])
        self.assertEqual(plan.exact_expectation(D), 18)
        self.assertEqual(plan.exact_expectation(lambda j: 1), 6)
        rev = WalkPlan(rels, ["R3", "R2", "R1"])
        self.assertEqual(rev.exact_expectation(D), 18)
        # In the reverse order every walk succeeds and has probability 1/6.
        rng = Random(1)
        self.assertEqual({rev.walk(rng, lambda j: 1)[0] for _ in range(200)}, {6})
        seen = {plan.walk(rng, lambda j: 1)[0] for _ in range(400)}
        self.assertEqual(seen, {0, 6, 12})

    def test_choose_plan_prefers_the_reverse_order(self):
        rels = page_example()
        plans = [WalkPlan(rels, ["R1", "R2", "R3"]), WalkPlan(rels, ["R3", "R2", "R1"])]
        self.assertEqual(choose_plan(plans, lambda j: 1, Random(2), tau=50), 1)


class TestUnbiased(unittest.TestCase):
    def test_exact_expectation_equals_the_join(self):
        rng = Random(3)
        for trial in range(30):
            shape = ["chain", "star", "cycle"][trial % 3]
            rels = random_instance(rng, shape)
            preds = {}
            if trial % 2:
                preds = {"S": lambda row: row["w_S"] % 3 != 0}
            for value in (lambda j: 1, weight_product):
                truth = brute_force_sum(rels, value, preds)
                for order in valid_orders(rels):
                    plan = WalkPlan(rels, order, preds)
                    self.assertEqual(plan.exact_expectation(value), truth, (shape, order))

    def test_monte_carlo_mean(self):
        rng = Random(4)
        covered = 0
        runs = 0
        for trial in range(12):
            rels = random_instance(rng, ["chain", "star", "cycle"][trial % 3])
            truth = float(brute_force_sum(rels, weight_product))
            order = next(iter(valid_orders(rels)))
            plan = WalkPlan(rels, order)
            for _ in range(5):
                est, half = wander_join(plan, weight_product, 600, rng)
                runs += 1
                if abs(est - truth) <= half:
                    covered += 1
                # four standard errors
                self.assertLessEqual(abs(est - truth), 4 * half / 1.96 + 1e-9)
        # the 95 percent intervals should cover the truth in most runs
        self.assertGreaterEqual(covered / runs, 0.8)

    def test_mean_of_many_walks(self):
        rels = page_example()
        plan = WalkPlan(rels, ["R1", "R2", "R3"])
        rng = Random(5)
        est, half = wander_join(plan, lambda j: j["D"], 20000, rng)
        self.assertLess(abs(est - 18), 0.6)
        self.assertLess(half, 0.6)

    def test_bad_order(self):
        rels = page_example()
        with self.assertRaises(ValueError):
            WalkPlan(rels, ["R1", "R3", "R2"])


if __name__ == "__main__":
    unittest.main()
