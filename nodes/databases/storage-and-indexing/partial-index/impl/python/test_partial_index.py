# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-index/. The authors are listed in prov/5RMQCY.jsonl.

import itertools
import random
import unittest

from partial_index import PartialIndex, Table, holds, implies, query

OPS = ["=", "<", "<=", ">", ">="]


def random_pred(rng, cols, n):
    return [(rng.choice(cols), rng.choice(OPS), rng.randrange(0, 6)) for _ in range(n)]


def orders(n, seed):
    rng = random.Random(seed)
    # status 0 = open (about 5%), 1 = shipped
    return [{"cust": rng.randrange(1000), "status": 0 if rng.random() < 0.05 else 1,
             "amount": rng.randrange(1, 500)} for _ in range(n)]


class TestImplication(unittest.TestCase):
    def test_against_brute_force_on_a_grid(self):
        rng = random.Random(1)
        grid = [dict(zip("ab", v)) for v in itertools.product(range(-2, 9), repeat=2)]
        for _ in range(3000):
            q = random_pred(rng, "ab", rng.randrange(0, 4))
            p = random_pred(rng, "ab", rng.randrange(0, 3))
            want = all(holds(p, r) for r in grid if holds(q, r))
            self.assertEqual(implies(q, p), want, (q, p))


class TestExample(unittest.TestCase):
    def test_open_orders(self):
        t = Table(orders(10000, 2))
        ix = PartialIndex(t, "cust", [("status", "=", 0)])
        n_open = sum(1 for r in t.rows.values() if r["status"] == 0)
        self.assertEqual(len(ix.entries), n_open)
        self.assertLess(len(ix.entries), 10000 // 10)
        ref = Table(orders(10000, 2))
        cases = [
            ([("status", "=", 0)], "index"),
            ([("status", "=", 0), ("amount", ">", 100)], "index"),
            ([], "scan"),
            ([("status", "<=", 0)], "scan"),             # status could be negative
            ([("status", "<=", 0), ("status", ">=", 0)], "index"),
            ([("status", "<", 2)], "scan"),
        ]
        for pred, plan in cases:
            got, used = query(t, "cust", 100, 199, pred, ix)
            want, _ = query(ref, "cust", 100, 199, pred)
            self.assertEqual(used, plan)
            self.assertEqual(got, want)


class TestAgainstFullScan(unittest.TestCase):
    def test_random_workload_with_changes(self):
        rng = random.Random(3)
        for seed in range(6):
            rows = [{"k": rng.randrange(50), "a": rng.randrange(6), "b": rng.randrange(6)}
                    for _ in range(300)]
            t, ref = Table(rows), Table(rows)
            p = random_pred(rng, "ab", rng.randrange(1, 3))
            ix = PartialIndex(t, "k", p)
            for step in range(200):
                r = rng.random()
                if r < 0.2:
                    row = {"k": rng.randrange(50), "a": rng.randrange(6), "b": rng.randrange(6)}
                    self.assertEqual(t.insert(row), ref.insert(row))
                elif r < 0.4 and t.rows:
                    rid = rng.choice(sorted(t.rows))
                    v = {rng.choice("kab"): rng.randrange(6)}
                    t.update(rid, **v)
                    ref.update(rid, **v)
                elif r < 0.45 and t.rows:
                    rid = rng.choice(sorted(t.rows))
                    t.delete(rid)
                    ref.delete(rid)
                else:
                    q = random_pred(rng, "ab", rng.randrange(0, 4))
                    lo = rng.randrange(50)
                    hi = lo + rng.randrange(20)
                    got, used = query(t, "k", lo, hi, q, ix)
                    want, _ = query(ref, "k", lo, hi, q)
                    self.assertEqual(got, want)
                    self.assertEqual(used == "index",
                                     implies(q + [("k", ">=", lo), ("k", "<=", hi)], p))
                # the index holds exactly the rows that satisfy p
                self.assertEqual(ix.entries, sorted((r["k"], rid) for rid, r in t.rows.items()
                                                    if holds(p, r)))

    def test_changes_outside_the_predicate_cost_no_index_work(self):
        t = Table(orders(2000, 4))
        PartialIndex(t, "cust", [("status", "=", 0)])
        shipped = [rid for rid, r in t.rows.items() if r["status"] == 1]
        for rid in shipped[:500]:
            t.update(rid, amount=7)
        self.assertEqual(t.stats["index_writes"], 0)
        open_ = [rid for rid, r in t.rows.items() if r["status"] == 0]
        t.update(open_[0], status=1)                 # the row leaves the index
        t.update(shipped[0], status=0)               # and another one enters it
        self.assertEqual(t.stats["index_writes"], 2)


if __name__ == "__main__":
    unittest.main()
