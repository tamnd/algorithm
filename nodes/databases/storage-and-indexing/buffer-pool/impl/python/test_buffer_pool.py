# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/buffer-pool/. The authors are listed in prov/GQQFSE.jsonl.

import random
import unittest

from buffer_pool import AllFramesPinned, BufferPool, Disk


def make_disk(n, size=8):
    return Disk({p: bytes([p % 256]) * size for p in range(n)})


def lru_misses(trace, b):
    """A plain LRU cache of b pages, as a list from least to most recent."""
    cache, misses = [], 0
    for p in trace:
        if p in cache:
            cache.remove(p)
        else:
            misses += 1
            if len(cache) == b:
                cache.pop(0)
        cache.append(p)
    return misses


def clock_misses(trace, b):
    """A plain CLOCK of b frames: free frames fill in order, then the hand sweeps."""
    pages, refs, hand, misses = [None] * b, [False] * b, 0, 0
    for p in trace:
        if p in pages:
            refs[pages.index(p)] = True
            continue
        misses += 1
        if None in pages:
            i = pages.index(None)
        else:
            while refs[hand]:
                refs[hand] = False
                hand = (hand + 1) % b
            i = hand
            hand = (hand + 1) % b
        pages[i], refs[i] = p, True
    return misses


def run(pool, trace):
    for p in trace:
        pool.fetch(p)
        pool.unpin(p)


class TestBufferPool(unittest.TestCase):
    def test_worked_example(self):
        trace = [1, 2, 3, 1, 4, 1, 2, 5, 1, 2]
        lru = BufferPool(make_disk(6), 3, "lru")
        run(lru, trace)
        self.assertEqual((lru.misses, lru.hits), (6, 4))
        self.assertEqual(lru.resident(), [1, 2, 5])
        clock = BufferPool(make_disk(6), 3, "clock")
        run(clock, trace)
        self.assertEqual((clock.misses, clock.hits), (7, 3))
        self.assertEqual(clock.resident(), [1, 2, 5])
        self.assertEqual(clock.disk.reads, 7)
        self.assertEqual(clock.disk.writes, 0)

    def test_policies_match_plain_simulations(self):
        for seed in range(20):
            rng = random.Random(seed)
            n = rng.randrange(2, 30)
            b = rng.randrange(1, 10)
            hot = max(1, n // 5)
            trace = [rng.randrange(hot) if rng.random() < 0.7 else rng.randrange(n)
                     for _ in range(400)]
            lru = BufferPool(make_disk(n), b, "lru")
            run(lru, trace)
            self.assertEqual(lru.misses, lru_misses(trace, b))
            self.assertEqual(lru.disk.reads, lru.misses)
            clock = BufferPool(make_disk(n), b, "clock")
            run(clock, trace)
            self.assertEqual(clock.misses, clock_misses(trace, b))

    def test_looping_scan_defeats_lru(self):
        # A loop over b + 1 pages misses on every access with LRU.
        trace = list(range(5)) * 10
        pool = BufferPool(make_disk(5), 4, "lru")
        run(pool, trace)
        self.assertEqual(pool.misses, len(trace))

    def test_all_pinned(self):
        pool = BufferPool(make_disk(4), 2)
        pool.fetch(0)
        pool.fetch(1)
        with self.assertRaises(AllFramesPinned):
            pool.fetch(2)
        self.assertEqual(pool.resident(), [0, 1])
        pool.unpin(1)
        pool.fetch(2)
        self.assertEqual(pool.resident(), [0, 2])
        pool.unpin(2)
        with self.assertRaises(ValueError):
            pool.unpin(2)

    def test_pinned_pages_stay_and_data_is_consistent(self):
        for seed in range(15):
            rng = random.Random(1000 + seed)
            n, b = rng.randrange(3, 20), rng.randrange(2, 6)
            policy = rng.choice(["lru", "clock"])
            disk = make_disk(n, 4)
            pool = BufferPool(disk, b, policy)
            truth = dict(disk.pages)
            pinned = {}
            dirty_evictions = 0
            for _ in range(300):
                p = rng.randrange(n)
                if pinned and rng.random() < 0.3:
                    q = rng.choice(sorted(pinned))
                    pool.unpin(q)
                    pinned[q] -= 1
                    if pinned[q] == 0:
                        del pinned[q]
                    continue
                before = set(pool.resident())
                dirty_before = {f.pid for f in pool.frames if f.dirty}
                try:
                    data = pool.fetch(p)
                except AllFramesPinned:
                    self.assertTrue(all(f.pin > 0 for f in pool.frames))
                    self.assertNotIn(p, pool.table)
                    continue
                gone = before - set(pool.resident())
                self.assertFalse(gone & set(pinned), "a pinned page was evicted")
                dirty_evictions += len(gone & dirty_before)
                self.assertEqual(bytes(data), truth[p])
                change = rng.random() < 0.5
                if change:
                    data[rng.randrange(4)] = rng.randrange(256)
                    truth[p] = bytes(data)
                if rng.random() < 0.4:
                    pinned[p] = pinned.get(p, 0) + 1
                    if change:
                        pool.frames[pool.table[p]].dirty = True
                else:
                    pool.unpin(p, dirty=change)
                for q, c in pinned.items():
                    self.assertEqual(pool.pin_count(q), c)
                pool.check()
            self.assertEqual(disk.writes, dirty_evictions)
            for q in list(pinned):
                for _ in range(pinned[q]):
                    pool.unpin(q)
            pool.flush_all()
            self.assertEqual(disk.pages, truth)
            writes = disk.writes
            pool.flush_all()
            self.assertEqual(disk.writes, writes)

    def test_new_page(self):
        disk = make_disk(2)
        pool = BufferPool(disk, 2)
        pid = pool.new_page(8)
        self.assertEqual(pid, 2)
        self.assertEqual(disk.reads, 0)
        pool.fetch(pid)[0] = 7
        pool.unpin(pid)
        pool.unpin(pid)
        pool.fetch(0)
        pool.unpin(0)
        pool.fetch(1)
        pool.unpin(1)
        self.assertEqual(disk.pages[2][0], 7)
        self.assertEqual(disk.writes, 1)


if __name__ == "__main__":
    unittest.main()
