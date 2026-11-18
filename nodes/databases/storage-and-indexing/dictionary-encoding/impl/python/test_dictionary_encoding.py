# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dictionary-encoding/. The authors are listed in prov/4407VK.jsonl.

import random
import unittest

import dbrel
from dictionary_encoding import DictColumn

CITIES = ["Paris", "Berlin", "Paris", "Rome", "Berlin", "Paris", None, "Athens"]
OPS = ["=", "<>", "<", "<=", ">", ">="]


def expected_positions(values, op, v):
    rel = dbrel.Relation(("pos", "v"), list(enumerate(values)))
    sel = dbrel.select(rel, lambda row: dbrel.cmp3(op, row["v"], v))
    return sorted(p for p, _ in sel.rows)


class TestDictionaryEncoding(unittest.TestCase):
    def test_worked_example(self):
        col = DictColumn(CITIES, ordered=True)
        self.assertEqual(col.D, ["Athens", "Berlin", "Paris", "Rome"])
        self.assertEqual(col.w, 3)
        self.assertEqual([col.code_at(i) for i in range(8)], [3, 2, 3, 4, 2, 3, 0, 1])
        self.assertEqual(col.size_bytes(), 3)
        self.assertEqual(col.code_range("<", "Paris"), range(1, 3))
        self.assertEqual(col.select("<", "Paris"), [1, 4, 7])
        self.assertEqual(col.code_range(">=", "Oslo"), range(3, 5))
        self.assertEqual(col.decodes, 0)
        self.assertEqual(col.decode_all(), CITIES)

        un = DictColumn(CITIES, ordered=False)
        self.assertEqual(un.D, ["Paris", "Berlin", "Rome", "Athens"])
        self.assertEqual([un.code_at(i) for i in range(8)], [1, 2, 1, 3, 2, 1, 0, 4])
        self.assertEqual(un.matching_codes("<", "Paris"), {2, 4})
        self.assertEqual(un.select("<", "Paris"), [1, 4, 7])
        self.assertEqual(un.compares, 8)
        self.assertEqual(un.decodes, 0)

    def test_round_trip_and_size(self):
        for seed in range(100):
            rng = random.Random(seed)
            n = rng.randrange(0, 300)
            d = rng.choice([1, 2, 3, 7, 8, 100, 1000])
            pool = [rng.randrange(-10 ** 6, 10 ** 6) for _ in range(d)]
            if rng.random() < 0.5:
                pool = [str(x) for x in pool]
            values = [None if rng.random() < 0.1 else rng.choice(pool) for _ in range(n)]
            for ordered in (True, False):
                col = DictColumn(values, ordered)
                self.assertEqual(col.decode_all(), values)
                distinct = len(set(v for v in values if v is not None))
                self.assertEqual(len(col.D), distinct)
                self.assertEqual(col.w, max(1, distinct.bit_length()))
                self.assertEqual(col.size_bytes(), (n * col.w + 7) // 8)

    def test_order_preservation(self):
        rng = random.Random(7)
        values = [rng.choice("abcdefghij") * rng.randrange(1, 3) for _ in range(200)]
        col = DictColumn(values, ordered=True)
        for i in range(0, 200, 7):
            for j in range(0, 200, 11):
                self.assertEqual(values[i] < values[j], col.code_at(i) < col.code_at(j))

    def test_selections_against_dbrel(self):
        for seed in range(150):
            rng = random.Random(500 + seed)
            n = rng.randrange(0, 80)
            values = [None if rng.random() < 0.15 else rng.randrange(20) for _ in range(n)]
            for ordered in (True, False):
                col = DictColumn(values, ordered)
                for _ in range(5):
                    op, v = rng.choice(OPS), rng.choice([None] + list(range(-2, 23)))
                    self.assertEqual(col.select(op, v), expected_positions(values, op, v),
                                     (ordered, op, v))
                self.assertEqual(col.decodes, 0)

    def test_unknown_operator(self):
        with self.assertRaises(ValueError):
            DictColumn([1, 2]).select("~", 1)


if __name__ == "__main__":
    unittest.main()
