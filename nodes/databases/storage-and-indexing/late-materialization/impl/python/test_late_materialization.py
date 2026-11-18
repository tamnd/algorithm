# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/late-materialization/. The authors are listed in prov/DADXAP.jsonl.

import random
import unittest

import dbrel
from late_materialization import ColumnTable, order_by_selectivity


def example():
    return ColumnTable({
        "region": ["EU", "US", "EU", "EU", "ASIA", "US", "EU", "ASIA"],
        "price": [10, 70, 80, 30, 20, 40, 45, 90],
        "qty": [1, 2, 3, 4, 5, 6, 7, 8],
    })


class TestLateMaterialization(unittest.TestCase):
    def test_worked_example(self):
        preds = [("region", "=", "EU"), ("price", "<", 50)]
        t = example()
        self.assertEqual(t.late(preds, ["qty"]), [(1,), (4,), (7,)])
        self.assertEqual(t.reads, 8 + 4 + 3)
        t = example()
        self.assertEqual(t.early(preds, ["qty"]), [(1,), (4,), (7,)])
        self.assertEqual(t.reads, 24)
        t = example()
        self.assertEqual(t.bitmap(preds, ["qty"]), [(1,), (4,), (7,)])
        self.assertEqual(t.reads, 8 + 8 + 3)
        t = example()
        t.late(list(reversed(preds)), ["qty"])
        self.assertEqual(t.reads, 8 + 5 + 3)
        self.assertEqual(order_by_selectivity(t, preds), preds)

    def test_results_against_dbrel(self):
        ops = ["=", "<>", "<", "<=", ">", ">="]
        for seed in range(200):
            rng = random.Random(seed)
            schema = ("a", "b", "c", "d")[:rng.randrange(1, 5)]
            rel = dbrel.random_relation(rng, schema, rng.randrange(0, 40), domain=5,
                                        null_rate=rng.choice([0.0, 0.2]))
            rows = [t for t in rel.sorted_rows()]
            rng.shuffle(rows)
            cols = {a: [t[j] for t in rows] for j, a in enumerate(schema)}
            preds = [(rng.choice(schema), rng.choice(ops), rng.randrange(5))
                     for _ in range(rng.randrange(0, 4))]
            out = [a for a in schema if rng.random() < 0.6] or [schema[0]]

            def pred(row, preds=preds):
                return all(dbrel.cmp3(op, row[c], v) is True for c, op, v in preds)

            expected = dbrel.project(dbrel.select(dbrel.Relation(schema, rows), pred), out)
            results = {}
            for name in ("late", "early", "bitmap"):
                table = ColumnTable(cols)
                results[name] = getattr(table, name)(preds, out)
                self.assertEqual(dbrel.Relation(out, results[name]), expected, name)
            # all three keep the records in position order
            self.assertEqual(results["late"], results["early"])
            self.assertEqual(results["late"], results["bitmap"])

    def test_read_counts(self):
        for seed in range(100):
            rng = random.Random(1000 + seed)
            n = rng.randrange(0, 60)
            cols = {c: [rng.randrange(10) for _ in range(n)] for c in "abcde"}
            preds = [(rng.choice("abcde"), rng.choice(["<", ">=", "="]), rng.randrange(10))
                     for _ in range(rng.randrange(1, 4))]
            out = rng.sample("abcde", rng.randrange(1, 4))
            sizes = []
            for m in range(len(preds)):
                sizes.append(len(ColumnTable(cols).positions(preds[:m + 1])))
            table = ColumnTable(cols)
            table.late(preds, out)
            self.assertEqual(table.reads, n + sum(sizes[:-1]) + sizes[-1] * len(out))
            table = ColumnTable(cols)
            table.early(preds, out)
            used = set(c for c, _, _ in preds) | set(out)
            self.assertEqual(table.reads, n * len(used))
            table = ColumnTable(cols)
            table.bitmap(preds, out)
            self.assertEqual(table.reads, n * len(preds) + sizes[-1] * len(out))

    def test_most_selective_first_reads_least(self):
        for seed in range(50):
            rng = random.Random(2000 + seed)
            n = 50
            cols = {c: [rng.randrange(10) for _ in range(n)] for c in "ab"}
            preds = [("a", "<", rng.randrange(10)), ("b", "<", rng.randrange(10))]
            best = order_by_selectivity(ColumnTable(cols), preds)
            t1, t2 = ColumnTable(cols), ColumnTable(cols)
            t1.late(best, ["a"])
            t2.late(list(reversed(best)), ["a"])
            self.assertLessEqual(t1.reads, t2.reads)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            ColumnTable({"a": [1], "b": []})
        with self.assertRaises(ValueError):
            example().late([("nope", "=", 1)], ["qty"])


if __name__ == "__main__":
    unittest.main()
