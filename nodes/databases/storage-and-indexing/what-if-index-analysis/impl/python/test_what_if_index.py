# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/what-if-index-analysis/. The authors are listed in prov/STWF16.jsonl.

import random
import statistics
import unittest

from what_if_index import Optimizer, Table, full_scan


def make_table(n, seed):
    rng = random.Random(seed)
    return Table([{"a": rng.randrange(10 ** 6), "b": int(rng.paretovariate(1.2)) % 5000}
                  for _ in range(n)])


def random_query(rng, col):
    lo = rng.randrange(10 ** 6) if col == "a" else rng.randrange(50)
    width = rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5]) if col == "a" else rng.randrange(0, 20)
    return col, lo, lo + width


class TestAgainstBuiltIndex(unittest.TestCase):
    def test_full_statistics_give_the_cost_of_the_built_index(self):
        """With statistics from all rows, the what-if cost equals the cost with the real index."""
        rng = random.Random(1)
        t = make_table(20000, 1)
        hypo = Optimizer(t)
        real = Optimizer(t)
        real.create_index("a")
        real.create_index("b")
        for _ in range(200):
            q = random_query(rng, rng.choice("ab"))
            self.assertEqual(hypo.what_if(q, [q[0]], fraction=1.0), real.cost(*q))

    def test_what_if_leaves_the_catalog_unchanged(self):
        t = make_table(5000, 2)
        opt = Optimizer(t)
        self.assertEqual(opt.cost("a", 10, 20)[1], "scan")
        c, plan = opt.what_if(("a", 10, 20), ["a"])
        self.assertEqual(plan, "index")
        self.assertEqual(opt.catalog, {})
        self.assertEqual(opt.stats, {})
        self.assertEqual(opt.cost("a", 10, 20)[1], "scan")

    def test_what_if_reads_only_a_sample(self):
        t = make_table(20000, 3)
        opt = Optimizer(t)
        opt.what_if(("a", 0, 100), ["a"], fraction=0.05)
        self.assertEqual(t.rows_read, 1000)
        opt.create_index("a")
        self.assertEqual(t.rows_read, 21000)


class TestAgainstFullScan(unittest.TestCase):
    def test_plans_on_built_indexes_return_the_scan_result(self):
        rng = random.Random(4)
        t = make_table(20000, 4)
        opt = Optimizer(t)
        opt.create_index("a")
        opt.create_index("b")
        plans = set()
        for _ in range(100):
            q = random_query(rng, rng.choice("ab"))
            rows, pages = opt.run(*q)
            plans.add(opt.cost(*q)[1])
            self.assertEqual(rows, full_scan(t, *q))
        self.assertEqual(plans, {"index", "scan"})

    def test_sampled_estimates_are_close_to_the_real_cost(self):
        """A measurement: on uniform data, a 5% sample predicts the pages read well."""
        rng = random.Random(5)
        t = make_table(20000, 5)
        opt = Optimizer(t)
        real = Optimizer(t)
        real.create_index("a")
        ratios = []
        for _ in range(200):
            col, lo, _ = random_query(rng, "a")
            q = (col, lo, lo + 10 ** 4)                  # about 1% of the rows
            est, plan = opt.what_if(q, ["a"], fraction=0.05, seed=rng.randrange(100))
            if plan == "index":
                _, pages = real.run(*q)
                ratios.append(est / pages)
        self.assertGreater(len(ratios), 150)
        self.assertLess(abs(statistics.median(ratios) - 1.0), 0.2)


if __name__ == "__main__":
    unittest.main()
