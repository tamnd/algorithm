# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alex-learned-index/. The authors are listed in prov/DS250H.jsonl.

import bisect
import random
import unittest

from alex_learned_index import ALEX, DataNode


class SortedList:
    """The reference: a plain sorted Python list."""

    def __init__(self, keys=()):
        self.a = sorted(set(keys))

    def insert(self, k):
        i = bisect.bisect_left(self.a, k)
        if i < len(self.a) and self.a[i] == k:
            return False
        self.a.insert(i, k)
        return True

    def delete(self, k):
        i = bisect.bisect_left(self.a, k)
        if i < len(self.a) and self.a[i] == k:
            del self.a[i]
            return True
        return False

    def range(self, lo, hi):
        return self.a[bisect.bisect_left(self.a, lo):bisect.bisect_right(self.a, hi)]


class TestDataNode(unittest.TestCase):
    def test_gapped_array_inserts(self):
        rng = random.Random(1)
        for trial in range(40):
            cap = rng.randrange(4, 40)
            keys = sorted(rng.sample(range(200), rng.randrange(0, cap // 2 + 1)))
            d = DataNode(keys, cap)
            ref = SortedList(keys)
            while d.n < cap:
                k = rng.randrange(-20, 220)
                self.assertEqual(d.insert(k), ref.insert(k))
                self.assertEqual(d.keys(), ref.a)
            for k in range(-25, 225):
                self.assertEqual(d.find(k)[0], k in ref.a)
            for k in list(ref.a)[::2] + [999]:
                self.assertEqual(d.delete(k), ref.delete(k))
                self.assertEqual(d.keys(), ref.a)

    def test_model_based_placement(self):
        d = DataNode([10, 20, 30, 40, 50, 60], 10)
        self.assertEqual([i for i in range(10) if d.occ[i]], [0, 2, 3, 5, 7, 8])
        self.assertEqual(d.vals, [10, 20, 20, 30, 40, 40, 50, 50, 60, float("inf")])
        self.assertEqual([d.predict(k) for k in (10, 35, 60)], [0, 4, 8])
        self.assertTrue(d.insert(35))       # slot 4 is the predicted slot and a gap
        self.assertEqual(d.vals[4], 35)
        self.assertTrue(d.insert(15))       # slot 1 is the predicted slot and a gap
        self.assertEqual(d.vals[1], 15)
        self.assertTrue(d.insert(33))       # no gap between 30 and 35: shift 35 and 40 right
        self.assertEqual([d.vals[i] for i in range(10) if d.occ[i]], [10, 15, 20, 30, 33, 35, 40, 50, 60])
        self.assertEqual([i for i in range(10) if not d.occ[i]], [9])
        self.assertFalse(d.insert(33))


class TestALEX(unittest.TestCase):
    def workload(self, seed, keyspace, n0, ops, **kw):
        rng = random.Random(seed)
        init = rng.sample(range(keyspace), n0)
        t = ALEX(init, **kw)
        ref = SortedList(init)
        t.check()
        for step in range(ops):
            r = rng.random()
            if r < 0.6:
                k = rng.randrange(keyspace)
                self.assertEqual(t.insert(k), ref.insert(k))
            elif r < 0.75:
                k = rng.choice(ref.a) if ref.a and rng.random() < 0.8 else rng.randrange(keyspace)
                self.assertEqual(t.delete(k), ref.delete(k))
            elif r < 0.9:
                k = rng.randrange(keyspace)
                self.assertEqual(t.contains(k), k in ref.a)
            else:
                lo = rng.randrange(keyspace)
                hi = lo + rng.randrange(keyspace // 20)
                self.assertEqual(t.range(lo, hi), ref.range(lo, hi))
            if step % 200 == 0:
                t.check()
        t.check()
        self.assertEqual(t.keys(), ref.a)
        return t

    def test_uniform_inserts(self):
        for seed in range(3):
            t = self.workload(seed, 10 ** 5, 200, 1500)
            self.assertGreater(t.splits, 0)
            self.assertGreater(t.expansions, 0)

    def test_skewed_inserts_split_down(self):
        rng = random.Random(7)
        t = ALEX(range(0, 400, 4), max_capacity=32, max_fanout=4)
        ref = SortedList(range(0, 400, 4))
        for _ in range(800):                 # all new keys fall in a narrow range
            k = 1000 + rng.randrange(2000)
            self.assertEqual(t.insert(k), ref.insert(k))
        t.check()
        self.assertEqual(t.keys(), ref.a)
        self.assertGreaterEqual(t.depth(), 3)
        for k in range(990, 3010, 7):
            self.assertEqual(t.contains(k), k in ref.a)

    def test_sequential_inserts(self):
        t = ALEX([], max_capacity=32, max_fanout=8)
        for k in range(600):
            self.assertTrue(t.insert(k))
        t.check()
        self.assertEqual(t.keys(), list(range(600)))
        self.assertFalse(t.insert(10))

    def test_lookups_are_short_on_linear_keys(self):
        keys = list(range(0, 30000, 3))
        t = ALEX(keys, max_capacity=256, max_fanout=1024)
        self.assertTrue(all(t.contains(k) for k in keys[::50]))
        worst = max(t.probes(k) for k in keys[::50])
        self.assertLessEqual(worst, 4)

    def test_bad_arguments(self):
        with self.assertRaises(ValueError):
            ALEX([], d_lower=0.9, d_upper=0.8)
        with self.assertRaises(ValueError):
            ALEX([], max_fanout=6)


if __name__ == "__main__":
    unittest.main()
