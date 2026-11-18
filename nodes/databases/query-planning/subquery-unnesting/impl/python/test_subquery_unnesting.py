# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subquery-unnesting/. The authors are listed in prov/0C9G7B.jsonl.

import random
import unittest

import dbrel
from dbrel import Relation
from subquery_unnesting import AGGS, OPS, general_unnest, kim_unnest, nested, null_aware_antijoin, unnest

CONDS = [("exists",), ("not_exists",), ("in",), ("not_in",)] + [("scalar", op, agg) for op in OPS for agg in AGGS]
R0 = Relation(("k", "x"), [(1, 0), (2, 0), (3, 2), (None, 0)])
S0 = Relation(("k", "v"), [(1, 5), (1, 7), (3, None), (None, 4)])


def random_tables(rng):
    R = dbrel.random_relation(rng, ["k", "x"], rng.randint(0, 5), domain={"k": [1, 2, 3], "x": [0, 1, 2]},
                              null_rate=0.2)
    S = dbrel.random_relation(rng, ["k", "v"], rng.randint(0, 5), domain={"k": [1, 2, 3], "v": [0, 1, 2]},
                              null_rate=0.2)
    return R, S


class TestUnnesting(unittest.TestCase):
    def test_rewrites_equal_the_nested_query(self):
        rng = random.Random(1)
        for _ in range(60):
            R, S = random_tables(rng)
            for cond in CONDS:
                want = nested(R, S, cond)
                self.assertEqual(unnest(R, S, cond), want, (R, S, cond))
                if cond[0] == "scalar":
                    self.assertEqual(general_unnest(R, S, cond), want, (R, S, cond))

    def test_count_bug(self):
        cond = ("scalar", "=", "count_star")
        self.assertEqual(nested(R0, S0, cond), Relation(("k", "x"), [(2, 0), (None, 0)]))
        self.assertEqual(kim_unnest(R0, S0, cond), Relation(("k", "x"), []))
        self.assertEqual(unnest(R0, S0, cond), nested(R0, S0, cond))
        self.assertEqual(nested(R0, S0, ("scalar", "=", "count")), Relation(("k", "x"), [(2, 0), (None, 0)]))

    def test_kim_is_right_when_the_empty_value_is_null(self):
        rng = random.Random(2)
        wrong = 0
        for _ in range(60):
            R, S = random_tables(rng)
            for op in OPS:
                for agg in ("sum", "min", "max"):
                    self.assertEqual(kim_unnest(R, S, ("scalar", op, agg)), nested(R, S, ("scalar", op, agg)))
                for agg in ("count_star", "count"):
                    wrong += kim_unnest(R, S, ("scalar", op, agg)) != nested(R, S, ("scalar", op, agg))
        self.assertGreater(wrong, 0)

    def test_not_in_with_nulls(self):
        naive = dbrel.antijoin(R0, dbrel.project(S0, ["k"]))
        self.assertEqual(naive, Relation(("k", "x"), [(2, 0), (None, 0)]))
        self.assertEqual(nested(R0, S0, ("not_in",)), Relation(("k", "x"), []))
        S1 = dbrel.select(S0, lambda s: s["k"] is not None)
        self.assertEqual(nested(R0, S1, ("not_in",)), Relation(("k", "x"), [(2, 0)]))
        self.assertEqual(null_aware_antijoin(R0, dbrel.project(S1, ["k"])), Relation(("k", "x"), [(2, 0)]))
        empty = Relation(("k", "v"), [])
        self.assertEqual(nested(R0, empty, ("not_in",)), R0)
        self.assertEqual(unnest(R0, empty, ("not_in",)), R0)
        self.assertEqual(nested(R0, S0, ("not_exists",)), naive)

    def test_exists_needs_a_semijoin(self):
        want = Relation(("k", "x"), [(1, 0), (3, 2)])
        self.assertEqual(nested(R0, S0, ("exists",)), want)
        self.assertEqual(unnest(R0, S0, ("exists",)), want)
        joined = dbrel.project(dbrel.natural_join(R0, S0), ["k", "x"])
        self.assertEqual(joined, Relation(("k", "x"), [(1, 0), (1, 0), (3, 2)]))

    def test_general_unnesting_needs_null_safe_join_back(self):
        cond = ("scalar", "=", "count_star")
        self.assertEqual(general_unnest(R0, S0, cond), nested(R0, S0, cond))
        self.assertEqual(general_unnest(R0, S0, cond, null_safe=False), Relation(("k", "x"), [(2, 0)]))

    def test_duplicates_in_the_outer_table(self):
        R = Relation(("k", "x"), [(1, 2), (1, 2), (2, 0), (2, 0), (2, 0)])
        for cond in CONDS:
            self.assertEqual(unnest(R, S0, cond), nested(R, S0, cond))
        self.assertEqual(len(unnest(R, S0, ("scalar", "=", "count_star"))), 5)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            nested(R0, S0, ("scalar", "==", "count"))
        with self.assertRaises(ValueError):
            unnest(R0, S0, ("scalar", "=", "avg_of"))
        with self.assertRaises(ValueError):
            unnest(Relation(("k", "y"), []), S0, ("exists",))
        with self.assertRaises(ValueError):
            unnest(R0.with_mode(dbrel.SET), S0, ("exists",))
        with self.assertRaises(ValueError):
            kim_unnest(R0, S0, ("exists",))


if __name__ == "__main__":
    unittest.main()
