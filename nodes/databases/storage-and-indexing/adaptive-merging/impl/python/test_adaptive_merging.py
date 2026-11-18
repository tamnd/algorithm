# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-merging/. The authors are listed in prov/4GVQ8M.jsonl.

import random
import unittest

from adaptive_merging import AdaptiveMergingIndex, full_scan


def keys(entries):
    return [k for k, _ in entries]


class TestExample(unittest.TestCase):
    def test_page_example(self):
        col = [27, 3, 14, 8, 30, 19, 5, 22, 11]
        ix = AdaptiveMergingIndex(col, 3)
        self.assertIsNone(ix.runs)
        self.assertEqual(keys(ix.range_query(10, 20)), [11, 14, 19])
        self.assertEqual([keys(r) for r in ix.runs], [[3, 27], [8, 30], [5, 22]])
        self.assertEqual(keys(ix.final), [11, 14, 19])
        self.assertEqual(ix.stats["moved"], 3)
        self.assertEqual(keys(ix.range_query(15, 25)), [19, 22])
        self.assertEqual(ix.stats["moved"], 4)              # only 22 was new
        self.assertEqual(ix.covered, [(10, 25)])
        self.assertEqual(keys(ix.range_query(0, 12)), [3, 5, 8, 11])
        self.assertEqual([keys(r) for r in ix.runs], [[27], [30]])
        self.assertEqual(keys(ix.final), [3, 5, 8, 11, 14, 19, 22])
        self.assertEqual(ix.covered, [(0, 25)])
        ix.check()


class TestAgainstFullScan(unittest.TestCase):
    def test_random_queries(self):
        for seed in range(8):
            rng = random.Random(seed)
            n = rng.randrange(1, 400)
            col = [rng.randrange(200) for _ in range(n)]        # many equal keys
            ix = AdaptiveMergingIndex(col, rng.randrange(1, 50))
            for _ in range(60):
                lo = rng.randrange(-20, 220)
                hi = lo + rng.randrange(0, 60)
                self.assertEqual(ix.range_query(lo, hi), full_scan(col, lo, hi))
                ix.check()
                # each entry is moved from a run to the final partition at most once
                self.assertEqual(ix.stats["moved"], len(ix.final))
                self.assertLessEqual(ix.stats["moved"], n)

    def test_whole_domain_ends_the_runs(self):
        rng = random.Random(3)
        col = [rng.randrange(10 ** 6) for _ in range(2000)]
        ix = AdaptiveMergingIndex(col, 128)
        ix.range_query(0, 10 ** 5)
        self.assertEqual(len(ix.runs), 16)
        self.assertEqual(ix.stats["sorted"], 2000)
        self.assertEqual(keys(ix.range_query(0, 10 ** 6)), sorted(col))
        self.assertEqual(ix.entries_left_in_runs(), 0)
        self.assertEqual(ix.runs, [])
        self.assertEqual(ix.stats["moved"], 2000)
        self.assertEqual(ix.stats["sorted"], 2000)           # the runs were made once

    def test_repeat_query_does_no_merge_work(self):
        rng = random.Random(4)
        col = [rng.randrange(1000) for _ in range(500)]
        ix = AdaptiveMergingIndex(col, 64)
        first = ix.range_query(100, 300)
        before = dict(ix.stats)
        self.assertEqual(ix.range_query(100, 300), first)
        self.assertEqual(ix.range_query(150, 200), full_scan(col, 150, 200))
        self.assertEqual(ix.stats["moved"], before["moved"])
        self.assertEqual(ix.stats["searches"], before["searches"])

    def test_gaps_against_brute_force(self):
        rng = random.Random(5)
        for _ in range(200):
            ix = AdaptiveMergingIndex([], 1)
            for _ in range(rng.randrange(5)):
                a = rng.randrange(30)
                ix._cover(a, a + rng.randrange(1, 8))
            lo = rng.randrange(-3, 35)
            hi = lo + rng.randrange(0, 15)
            got = [x for a, b in ix.gaps(lo, hi) for x in range(a, b)]
            want = [x for x in range(lo, hi) if not any(c <= x < d for c, d in ix.covered)]
            self.assertEqual(got, want)
            for (a, b), (c, d) in zip(ix.gaps(lo, hi), ix.gaps(lo, hi)[1:]):
                self.assertLess(b, c)                         # gaps are separated


if __name__ == "__main__":
    unittest.main()
