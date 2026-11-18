# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-search-tree/. The authors are listed in prov/SE99CH.jsonl.

import random
import unittest

from generalized_search_tree import GiST, IntervalExt, RectExt


def scan(records, ext, q):
    """The brute force answer: every record whose exact key is consistent with q."""
    return sorted(r for r, k in records.items() if ext.consistent(k, q))


def random_interval(rng, span=100, width=6):
    a = rng.randrange(span)
    return (a, a + rng.randrange(width))


def random_rect(rng, span=60, size=8):
    x, y = rng.randrange(span), rng.randrange(span)
    return (x, y, x + rng.randrange(size), y + rng.randrange(size))


class TestGiST(unittest.TestCase):
    def run_workload(self, ext, make_key, seed, n, M, m):
        rng = random.Random(seed)
        t = GiST(ext, max_entries=M, min_entries=m)
        live = {}
        for i in range(n):
            k = make_key(rng)
            t.insert(k, i)
            live[i] = k
            if rng.random() < 0.3 and live:
                victim = rng.choice(sorted(live))
                self.assertTrue(t.delete(victim))
                del live[victim]
            if i % 25 == 0:
                t.check()
        t.check()
        for _ in range(40):
            q = make_key(rng)
            self.assertEqual(t.search(q), scan(live, ext, q))
        return t, live

    def test_interval_instance_like_a_b_plus_tree(self):
        for seed in range(6):
            self.run_workload(IntervalExt(), random_interval, seed, 150, 4, 2)
            self.run_workload(IntervalExt(), lambda r: (lambda x: (x, x))(r.randrange(200)),
                              seed + 100, 150, 5, 3)

    def test_rect_instance_like_an_r_tree(self):
        for seed in range(5):
            self.run_workload(RectExt(), random_rect, seed, 150, 4, 2)

    def test_lossy_compression_needs_the_recheck(self):
        ext = RectExt(grid=8)
        for seed in range(4):
            t, live = self.run_workload(ext, random_rect, seed, 120, 6, 3)
        # Without the recheck the leaves give false positives.
        rng = random.Random(9)
        t = GiST(RectExt(grid=8), 4, 2)
        for i in range(100):
            t.insert(random_rect(rng), i)
        false_pos = 0
        for _ in range(40):
            q = random_rect(rng, size=3)
            raw = []
            t._search(t.root, q, raw)
            exact = scan(t.records, t.ext, q)
            self.assertTrue(set(exact) <= set(raw))
            false_pos += len(raw) - len(exact)
        self.assertGreater(false_pos, 0)

    def test_point_query_prunes(self):
        t = GiST(IntervalExt(), 4, 2)
        for x in range(64):
            t.insert((x, x), x)
        t.check()
        self.assertEqual(t.search((37, 37)), [37])
        self.assertLessEqual(t.visited, 3 * t.height())
        self.assertEqual(t.search((10, 13)), [10, 11, 12, 13])

    def test_delete_everything(self):
        rng = random.Random(3)
        t = GiST(RectExt(), 4, 2)
        keys = {i: random_rect(rng) for i in range(60)}
        for i, k in keys.items():
            t.insert(k, i)
        order = list(keys)
        rng.shuffle(order)
        for i in order:
            self.assertTrue(t.delete(i))
            t.check()
        self.assertFalse(t.delete(0))
        self.assertEqual(t.search((0, 0, 100, 100)), [])
        self.assertTrue(t.root.leaf)

    def test_bad_arguments(self):
        with self.assertRaises(ValueError):
            GiST(IntervalExt(), 4, 3)
        t = GiST(IntervalExt(), 4, 2)
        t.insert((1, 1), "a")
        with self.assertRaises(KeyError):
            t.insert((2, 2), "a")


if __name__ == "__main__":
    unittest.main()
