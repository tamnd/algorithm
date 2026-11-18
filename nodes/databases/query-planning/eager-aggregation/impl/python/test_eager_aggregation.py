# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eager-aggregation/. The authors are listed in prov/B4N0ZP.jsonl.

import random
import unittest
from fractions import Fraction

import dbrel
from dbrel import Relation
from eager_aggregation import FUNCS, eager, eager_without_final, join_sizes, lazy

ALL = [("count_star", None, "n")] + [(f, a, "%s_%s" % (f, a)) for f in FUNCS if f != "count_star" for a in ("v", "x")]
R0 = Relation(("g", "k", "x"), [("a", 1, 10), ("a", 2, 20), ("b", 2, None), ("b", None, 5)])
S0 = Relation(("k", "v"), [(1, 3), (1, None), (2, 4), (2, 4), (2, 6), (None, 7)])


def random_tables(rng, key_g=False):
    n = rng.randint(0, 6)
    R = dbrel.random_relation(rng, ["g", "k", "x"], n, domain={"g": [0, 1, 2], "k": [1, 2, 3], "x": [0, 1, 2, 3]},
                              null_rate=0.15)
    if key_g:
        R = Relation(R.schema, [(i,) + t[1:] for i, t in enumerate(R.sorted_rows())])
    S = dbrel.random_relation(rng, ["k", "v"], rng.randint(0, 7), domain={"k": [1, 2, 3], "v": [0, 1, 2, 5]},
                              null_rate=0.15)
    return R, S


class TestEagerAggregation(unittest.TestCase):
    def test_eager_equals_lazy(self):
        rng = random.Random(1)
        for _ in range(150):
            R, S = random_tables(rng)
            for group in (["g"], []):
                self.assertEqual(eager(R, S, group, ALL), lazy(R, S, group, ALL), (R, S, group))
                aggs = rng.sample(ALL, rng.randint(1, 3))
                self.assertEqual(eager(R, S, group, aggs), lazy(R, S, group, aggs), (R, S, group, aggs))

    def test_worked_example(self):
        aggs = [("count_star", None, "n"), ("sum", "v", "sv"), ("sum", "x", "sx"), ("count", "x", "cx"),
                ("avg", "v", "av")]
        want = Relation(("g", "n", "sv", "sx", "cx", "av"),
                        [("a", 5, 17, 80, 5, Fraction(17, 4)), ("b", 3, 14, None, 0, Fraction(14, 3))])
        self.assertEqual(lazy(R0, S0, ["g"], aggs), want)
        self.assertEqual(eager(R0, S0, ["g"], aggs), want)
        P = dbrel.aggregate(S0, ["k"], [("count_star", None, "c"), ("sum", "v", "s"), ("count", "v", "m")])
        self.assertEqual(P, Relation(("k", "c", "s", "m"), [(None, 1, 7, 1), (1, 2, 3, 1), (2, 3, 14, 3)]))
        self.assertEqual(join_sizes(R0, S0), (8, 3))

    def test_naive_finals_are_wrong(self):
        P = dbrel.aggregate(S0, ["k"], [("count_star", None, "c"), ("avg", "v", "a")])
        J = dbrel.natural_join(R0, P)
        count_rows = dbrel.aggregate(J, ["g"], [("count_star", None, "n")])
        self.assertEqual(count_rows, Relation(("g", "n"), [("a", 2), ("b", 1)]))
        unweighted = dbrel.aggregate(J, ["g"], [("sum", "x", "sx")])
        self.assertEqual(unweighted, Relation(("g", "sx"), [("a", 30), ("b", None)]))
        avg_of_avgs = dbrel.aggregate(J, ["g"], [("avg", "a", "av")])
        self.assertEqual(avg_of_avgs, Relation(("g", "av"), [("a", Fraction(23, 6)), ("b", Fraction(14, 3))]))
        self.assertNotEqual(avg_of_avgs, lazy(R0, S0, ["g"], [("avg", "v", "av")]))

    def test_dropping_the_final_grouping(self):
        rng = random.Random(2)
        for _ in range(150):
            R, S = random_tables(rng, key_g=True)
            self.assertEqual(eager_without_final(R, S, ALL), lazy(R, S, ["g"], ALL), (R, S))
        aggs = [("count_star", None, "n"), ("sum", "v", "sv")]
        self.assertEqual(eager_without_final(R0, S0, aggs), Relation(("g", "n", "sv"), [("a", 2, 3), ("a", 3, 14),
                                                                                        ("b", 3, 14)]))
        self.assertNotEqual(eager_without_final(R0, S0, aggs), lazy(R0, S0, ["g"], aggs))

    def test_no_grouping_and_an_empty_join(self):
        R = Relation(("g", "k", "x"), [("a", None, 1), ("b", 9, 2)])
        want = Relation(("n", "count_v", "sum_v", "avg_x"), [(0, 0, None, None)])
        aggs = [("count_star", None, "n"), ("count", "v", "count_v"), ("sum", "v", "sum_v"), ("avg", "x", "avg_x")]
        self.assertEqual(lazy(R, S0, [], aggs), want)
        self.assertEqual(eager(R, S0, [], aggs), want)
        self.assertEqual(eager(R, S0, ["g"], aggs), Relation(("g", "n", "count_v", "sum_v", "avg_x"), []))

    def test_the_join_reads_fewer_rows(self):
        rng = random.Random(3)
        for _ in range(100):
            R, S = random_tables(rng)
            before, after = join_sizes(R, S)
            self.assertLessEqual(after, min(before, len(R)))

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            eager(R0, S0, ["k"], ALL)
        with self.assertRaises(ValueError):
            eager(R0, S0, ["g"], [("median", "v", "m")])
        with self.assertRaises(ValueError):
            eager(R0, S0, ["g"], [("sum", "k", "s")])
        with self.assertRaises(ValueError):
            eager(R0, S0, ["g"], [("count_star", "v", "n")])
        with self.assertRaises(ValueError):
            eager(R0, S0, ["g"], [("sum", "v", "c")])
        with self.assertRaises(ValueError):
            lazy(Relation(("g", "k"), []), S0, ["g"], ALL)
        with self.assertRaises(ValueError):
            eager(R0, S0.with_mode(dbrel.SET), ["g"], ALL)


if __name__ == "__main__":
    unittest.main()
