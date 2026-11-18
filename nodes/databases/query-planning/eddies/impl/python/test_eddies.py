# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eddies/. The authors are listed in prov/CC4NGE.jsonl.

import itertools
import unittest
from collections import Counter
from random import Random

from eddies import Eddy, FixedPolicy, LotteryPolicy, RandomPolicy, random_arrivals


def canon(parts):
    return tuple(sorted((r, id(row)) for r, row in parts.items()))


def brute_force(schemas, relations, filters):
    """The bag of results of the filtered natural join, by nested loops."""
    names = sorted(schemas)
    out = Counter()
    for combo in itertools.product(*(relations[n] for n in names)):
        parts = dict(zip(names, combo))
        if any(not pred(parts[rel]) for rel, pred in filters.values()):
            continue
        ok = all(parts[a][x] == parts[b][x]
                 for a, b in itertools.combinations(names, 2)
                 for x in set(schemas[a]) & set(schemas[b]))
        if ok:
            out[canon(parts)] += 1
    return out


SHAPES = {
    "chain": {"R": "ab", "S": "bc", "T": "cd"},
    "star": {"R": "ab", "S": "bc", "T": "bd", "U": "de"},
    "cycle": {"R": "ab", "S": "bc", "T": "ca"},
    "single": {"R": "ab"},
}


def instance(rng, shape):
    # the attribute w_<relation> is private to one relation, so it is not a join attribute
    schemas = {r: list(a) + ["w_" + r] for r, a in SHAPES[shape].items()}
    dom = rng.randint(2, 3)
    relations = {r: [{a: rng.randrange(dom) for a in schema} for _ in range(rng.randint(3, 7))]
                 for r, schema in schemas.items()}
    # rows are distinct objects even when their values repeat, so the join is a bag join
    filters = {}
    if rng.random() < 0.7:
        filters["f1"] = ("R", lambda row: row["w_R"] != 0)
    if rng.random() < 0.5:
        last = sorted(schemas)[-1]
        attr = schemas[last][0]
        filters["f2"] = (last, lambda row: row[attr] != 1)
    return schemas, relations, filters


def policies(names, filters):
    ops = list(filters) + ["stem:" + r for r in names]
    return [LotteryPolicy(), RandomPolicy(), FixedPolicy(ops), FixedPolicy(ops[::-1])]


class TestResults(unittest.TestCase):
    def test_same_bag_for_every_policy_and_order(self):
        rng = Random(1)
        for trial in range(60):
            shape = ["chain", "star", "cycle", "single"][trial % 4]
            schemas, relations, filters = instance(rng, shape)
            truth = brute_force(schemas, relations, filters)
            for policy in policies(list(schemas), filters):
                for p_route in (0.2, 0.6, 1.0):
                    eddy = Eddy(schemas, filters)
                    out = eddy.run(random_arrivals(relations, rng), policy, rng, p_route=p_route)
                    got = Counter(canon(p) for p in out)
                    self.assertEqual(got, truth, (shape, type(policy).__name__, p_route))
                    self.assertTrue(all(c == 1 for c in got.values()))

    def test_without_timestamps_results_repeat(self):
        rng = Random(5)
        repeated = 0
        for trial in range(40):
            schemas, relations, filters = instance(rng, ["chain", "star", "cycle"][trial % 3])
            truth = brute_force(schemas, relations, filters)
            out = Eddy(schemas, filters).run(random_arrivals(relations, rng), RandomPolicy(), rng,
                                             p_route=0.3, use_timestamps=False)
            got = Counter(canon(p) for p in out)
            # every result is still found, but some are found more than once
            self.assertEqual(set(got), set(truth))
            repeated += sum(got.values()) > sum(truth.values())
        self.assertGreater(repeated, 0)

    def test_one_relation_at_a_time(self):
        # all of R arrives first, then all of S, then all of T: the plan of a static pipeline
        rng = Random(2)
        schemas, relations, filters = instance(rng, "chain")
        arrivals = [(r, row) for r in ["R", "S", "T"] for row in relations[r]]
        got = Counter(canon(p) for p in Eddy(schemas, filters).run(arrivals, LotteryPolicy(), rng))
        self.assertEqual(got, brute_force(schemas, relations, filters))

    def test_example_of_the_page(self):
        schemas = {"R": ["a", "b"], "S": ["b", "c"]}
        r1, r2 = {"a": 1, "b": 7}, {"a": 2, "b": 8}
        s1, s2 = {"b": 7, "c": 3}, {"b": 7, "c": 4}
        arrivals = [("R", r1), ("S", s1), ("R", r2), ("S", s2)]
        out = Eddy(schemas).run(arrivals, RandomPolicy(), Random(0), p_route=1.0)
        # (r1, s1) is built when s1 arrives, and (r1, s2) when s2 arrives; r2 joins nothing
        self.assertEqual([(p["R"], p["S"]) for p in out], [(r1, s1), (r1, s2)])
        # all four tuples arrive before any routing: r1 must not probe S, or both results repeat
        out = Eddy(schemas).run(arrivals, RandomPolicy(), Random(0), p_route=0.0)
        self.assertEqual(sorted((p["S"]["c"]) for p in out), [3, 4])
        out = Eddy(schemas).run(arrivals, RandomPolicy(), Random(0), p_route=0.0, use_timestamps=False)
        self.assertEqual(sorted((p["S"]["c"]) for p in out), [3, 3, 4, 4])

    def test_disconnected_query(self):
        with self.assertRaises(ValueError):
            Eddy({"R": ["a"], "S": ["b"]})


class TestAdaptivity(unittest.TestCase):
    def run_filters(self, policy, seed):
        rng = Random(seed)
        rows = [{"x": rng.random(), "y": rng.random()} for _ in range(3000)]
        filters = {"cheap_pass": ("R", lambda r: r["x"] < 0.9), "rare_pass": ("R", lambda r: r["y"] < 0.1)}
        eddy = Eddy({"R": ["x", "y"]}, filters)
        out = eddy.run([("R", r) for r in rows], policy, rng)
        return len(out), sum(eddy.work.values())

    def test_lottery_learns_the_selective_filter(self):
        n_good, w_good = self.run_filters(FixedPolicy(["rare_pass", "cheap_pass"]), 3)
        n_bad, w_bad = self.run_filters(FixedPolicy(["cheap_pass", "rare_pass"]), 3)
        n_lot, w_lot = self.run_filters(LotteryPolicy(), 3)
        self.assertEqual(n_good, n_bad)
        self.assertEqual(n_good, n_lot)
        # about 3300 and 5700 filter calls for the two fixed orders
        self.assertLess(w_good, 3500)
        self.assertGreater(w_bad, 5400)
        self.assertLess(w_lot, w_good + 400)

    def test_lottery_tickets(self):
        policy = LotteryPolicy()
        self.run_filters(policy, 4)
        self.assertGreater(policy.tickets["rare_pass"], 10 * policy.tickets["cheap_pass"])


if __name__ == "__main__":
    unittest.main()
