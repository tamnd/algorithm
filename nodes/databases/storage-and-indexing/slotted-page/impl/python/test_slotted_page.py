# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slotted-page/. The authors are listed in prov/C42FG6.jsonl.

import random
import unittest

from slotted_page import HEADER, SLOT, PageFull, SlottedPage


class TestSlottedPage(unittest.TestCase):
    def test_empty_page(self):
        p = SlottedPage(64)
        self.assertEqual(p.n_slots, 0)
        self.assertEqual(p.free_end, 64)
        self.assertEqual(p.contiguous_free(), 64 - HEADER)
        self.assertIsNone(p.get(0))
        p.check()

    def test_layout_grows_from_both_ends(self):
        p = SlottedPage(64)
        a = p.insert(b"aaaaaaaaaa")
        b = p.insert(b"bbbbbb")
        self.assertEqual((a, b), (0, 1))
        self.assertEqual(p._slot(0), (54, 10))
        self.assertEqual(p._slot(1), (48, 6))
        self.assertEqual(p.free_end, 48)
        self.assertEqual(p.contiguous_free(), 48 - HEADER - 2 * SLOT)

    def test_worked_example(self):
        # The example on the page: P = 64, three inserts, a delete, a reuse, a compaction.
        p = SlottedPage(64)
        p.insert(b"A" * 10)
        p.insert(b"B" * 6)
        p.insert(b"C" * 12)
        self.assertEqual(p.free_end, 36)
        self.assertEqual(p.contiguous_free(), 20)
        p.delete(1)
        self.assertEqual(p.n_slots, 3)
        self.assertEqual(p.total_free(), 26)
        self.assertEqual(p.contiguous_free(), 20)
        s = p.insert(b"D" * 24)
        self.assertEqual(s, 1)
        self.assertEqual(p.compactions, 1)
        self.assertEqual(p._slot(0), (54, 10))
        self.assertEqual(p._slot(2), (42, 12))
        self.assertEqual(p._slot(1), (18, 24))
        self.assertEqual(p.contiguous_free(), 2)
        self.assertEqual(p.get(0), b"A" * 10)
        self.assertEqual(p.get(2), b"C" * 12)
        p.check()

    def test_trailing_free_slots_are_dropped(self):
        p = SlottedPage(128)
        for i in range(4):
            p.insert(bytes([i]) * 5)
        p.delete(1)
        p.delete(3)
        self.assertEqual(p.n_slots, 3)
        p.delete(2)
        self.assertEqual(p.n_slots, 1)
        p.check()

    def test_page_full(self):
        p = SlottedPage(32)
        p.insert(b"x" * 20)
        with self.assertRaises(PageFull):
            p.insert(b"y" * 5)
        self.assertEqual(p.records(), {0: b"x" * 20})
        self.assertEqual(p.insert(b""), 1)
        self.assertEqual(p.contiguous_free(), 0)
        p.check()

    def test_delete_missing(self):
        p = SlottedPage(64)
        with self.assertRaises(KeyError):
            p.delete(0)
        p.insert(b"a")
        p.delete(0)
        with self.assertRaises(KeyError):
            p.delete(0)

    def test_update_keeps_slot(self):
        p = SlottedPage(64)
        p.insert(b"a" * 10)
        p.insert(b"b" * 10)
        p.insert(b"c" * 10)
        p.update(1, b"B" * 3)
        self.assertEqual(p.get(1), b"B" * 3)
        p.update(1, b"Z" * 20)
        self.assertEqual(p.get(1), b"Z" * 20)
        self.assertEqual(p.records(), {0: b"a" * 10, 1: b"Z" * 20, 2: b"c" * 10})
        with self.assertRaises(PageFull):
            p.update(0, b"q" * 40)
        self.assertEqual(p.get(0), b"a" * 10)
        p.check()

    def test_random_against_dict(self):
        for seed in range(30):
            rng = random.Random(seed)
            size = rng.choice([64, 128, 256, 1024])
            p = SlottedPage(size)
            oracle = {}
            for _ in range(400):
                op = rng.random()
                if op < 0.45:
                    rec = bytes(rng.randrange(256) for _ in range(rng.randrange(0, size // 6)))
                    before = p.total_free()
                    free_slot = any(p.get(t) is None for t in range(p.n_slots))
                    need = len(rec) + (0 if free_slot else SLOT)
                    try:
                        s = p.insert(rec)
                    except PageFull:
                        self.assertGreater(need, before)
                        continue
                    self.assertLessEqual(need, before)
                    self.assertNotIn(s, oracle)
                    self.assertEqual(s, min(set(range(len(oracle) + 1)) - set(oracle)))
                    oracle[s] = rec
                elif op < 0.75 and oracle:
                    s = rng.choice(sorted(oracle))
                    p.delete(s)
                    del oracle[s]
                elif op < 0.95 and oracle:
                    s = rng.choice(sorted(oracle))
                    rec = bytes(rng.randrange(256) for _ in range(rng.randrange(0, size // 5)))
                    grow = len(rec) - len(oracle[s])
                    before = p.total_free()
                    try:
                        p.update(s, rec)
                    except PageFull:
                        self.assertGreater(grow, before)
                        continue
                    oracle[s] = rec
                else:
                    p.compact()
                    self.assertEqual(p.contiguous_free(), p.total_free())
                p.check()
                self.assertEqual(p.records(), oracle)
                used = sum(len(r) for r in oracle.values())
                self.assertEqual(p.total_free(), size - HEADER - SLOT * p.n_slots - used)
                self.assertEqual(p.n_slots, max(oracle) + 1 if oracle else 0)


if __name__ == "__main__":
    unittest.main()
