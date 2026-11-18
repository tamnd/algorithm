# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-of-reference-encoding/. The authors are listed in prov/PWP268.jsonl.

import random
import unittest

import dbrel
from frame_of_reference_encoding import HEADER_BYTES, FORColumn

EXAMPLE = [1000, 1003, 1001, 1007, 1012, 1010, 1015, 1011, 1020, 1020, 1020, 1020]
OPS = ["=", "<", "<=", ">", ">="]


def relation(values):
    return dbrel.Relation(("pos", "v"), list(enumerate(values)))


def expected_range(values, lo, hi):
    def pred(row):
        a = True if lo is None else dbrel.cmp3(">=", row["v"], lo)
        b = True if hi is None else dbrel.cmp3("<=", row["v"], hi)
        return dbrel.tv_and(a, b)
    return sorted(p for p, _ in dbrel.select(relation(values), pred).rows)


def expected_op(values, op, v):
    sel = dbrel.select(relation(values), lambda row: dbrel.cmp3(op, row["v"], v))
    return sorted(p for p, _ in sel.rows)


class TestFrameOfReference(unittest.TestCase):
    def test_worked_example(self):
        col = FORColumn(EXAMPLE, B=4)
        heads = [(b.base, b.max, b.w) for b in col.blocks]
        self.assertEqual(heads, [(1000, 1007, 3), (1010, 1015, 3), (1020, 1020, 0)])
        self.assertEqual([col.blocks[1].offset(j) for j in range(4)], [2, 0, 5, 1])
        self.assertEqual([len(b.bits) for b in col.blocks], [2, 2, 0])
        self.assertEqual(col.size_bytes(), 3 * HEADER_BYTES + 4)
        self.assertEqual(col.get(6), 1015)
        self.assertEqual(col.offsets_read, 1)

        col.offsets_read = 0
        self.assertEqual(col.select(1011, 1016), [4, 6, 7])
        self.assertEqual(col.blocks_skipped, 2)
        self.assertEqual(col.offsets_read, 4)

        col.offsets_read = col.blocks_skipped = 0
        self.assertEqual(col.select(1000, 1020), list(range(12)))
        self.assertEqual((col.offsets_read, col.blocks_skipped), (0, 0))
        self.assertEqual(col.decode_all(), EXAMPLE)

    def test_round_trip_and_size(self):
        for seed in range(150):
            rng = random.Random(seed)
            n = rng.randrange(0, 400)
            B = rng.choice([1, 2, 7, 64, 128])
            spread = rng.choice([0, 1, 5, 300, 10 ** 6, 2 ** 70])
            start = rng.randrange(-10 ** 9, 10 ** 9)
            values = [start + rng.randrange(spread + 1) for _ in range(n)]
            col = FORColumn(values, B)
            self.assertEqual(col.decode_all(), values)
            self.assertEqual([col.get(i) for i in range(n)], values)
            self.assertEqual(len(col.blocks), (n + B - 1) // B)
            for k, blk in enumerate(col.blocks):
                part = values[k * B:(k + 1) * B]
                self.assertEqual(blk.base, min(part))
                self.assertEqual(blk.w, (max(part) - min(part)).bit_length())
                self.assertEqual(len(blk.bits), (len(part) * blk.w + 7) // 8)

    def test_sorted_input_has_small_widths(self):
        values = list(range(0, 4096 * 3, 3))
        col = FORColumn(values, B=128)
        self.assertTrue(all(b.w == (127 * 3).bit_length() for b in col.blocks))
        self.assertEqual(col.size_bytes(), 32 * (HEADER_BYTES + 128 * 9 // 8))

    def test_selections_against_dbrel(self):
        for seed in range(200):
            rng = random.Random(1000 + seed)
            n = rng.randrange(0, 120)
            B = rng.choice([1, 3, 8, 16])
            if rng.random() < 0.5:
                values = sorted(rng.randrange(-50, 50) for _ in range(n))
            else:
                values = [rng.randrange(-50, 50) for _ in range(n)]
            col = FORColumn(values, B)
            for _ in range(6):
                lo = rng.choice([None] + list(range(-60, 60)))
                hi = rng.choice([None] + list(range(-60, 60)))
                self.assertEqual(col.select(lo, hi), expected_range(values, lo, hi), (lo, hi))
                op, v = rng.choice(OPS), rng.randrange(-60, 60)
                self.assertEqual(col.select_op(op, v), expected_op(values, op, v), (op, v))

    def test_skipping_on_sorted_input(self):
        values = list(range(1000))
        col = FORColumn(values, B=100)
        self.assertEqual(col.select(250, 349), list(range(250, 350)))
        self.assertEqual(col.blocks_skipped, 8)
        self.assertEqual(col.offsets_read, 200)

    def test_errors(self):
        with self.assertRaises(TypeError):
            FORColumn([1, 2.5])
        with self.assertRaises(ValueError):
            FORColumn([1], B=0)
        with self.assertRaises(ValueError):
            FORColumn([1]).select_op("<>", 1)
        with self.assertRaises(IndexError):
            FORColumn([1]).get(1)


if __name__ == "__main__":
    unittest.main()
