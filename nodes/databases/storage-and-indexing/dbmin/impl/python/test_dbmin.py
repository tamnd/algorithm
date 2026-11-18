# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dbmin/. The authors are listed in prov/DPJZ9M.jsonl.

import random
import unittest

from dbmin import DBMIN


def plain_cache(trace, l, policy):
    """A stand-alone cache of l pages; returns its contents after each request."""
    cache, states = [], []
    for p in trace:
        if p in cache:
            if policy != "fifo":
                cache.remove(p)
                cache.append(p)
        else:
            if len(cache) == l:
                cache.pop(-1 if policy == "mru" else 0)
            cache.append(p)
        states.append(sorted(cache))
    return states


def reference_model(n_frames, sets, trace):
    """A direct model of the three cases, with lists; returns the number of reads."""
    owner, free, members, reads = {}, [None] * n_frames, {s: [] for s in sets}, 0
    for sid, p in trace:
        l, policy = sets[sid]
        if p in owner and owner[p] == sid:
            if policy != "fifo":
                members[sid].remove(p)
                members[sid].append(p)
            continue
        if p in owner and owner[p] is not None:
            continue
        if p in owner:
            free.remove(p)
        else:
            old = free.pop(0)
            if old is not None:
                del owner[old]
            reads += 1
        if len(members[sid]) == l:
            v = members[sid].pop(-1 if policy == "mru" else 0)
            owner[v] = None
            free.append(v)
        members[sid].append(p)
        owner[p] = sid
    return reads


class TestDBMIN(unittest.TestCase):
    def test_worked_example_looping_scan(self):
        trace = list(range(6)) * 3
        reads = {}
        for policy in ("mru", "lru"):
            db = DBMIN(4)
            self.assertTrue(db.start("Q", {"R": (3, policy)}))
            for p in trace:
                db.request("Q", "R", p)
                db.check()
            reads[policy] = db.reads
        self.assertEqual(reads, {"mru": 12, "lru": 18})

    def test_worked_example_admission(self):
        db = DBMIN(10)
        self.assertTrue(db.start("Q1", {"R": (1, "fifo"), "S": (6, "mru")}))
        self.assertFalse(db.start("Q2", {"T": (3, "lru")}))   # 7 + 3 = 10 is not below 10
        self.assertFalse(db.start("Q3", {"U": (1, "fifo")}))  # it waits behind Q2
        self.assertEqual(db.finish("Q1"), ["Q2", "Q3"])
        self.assertEqual(db.demand(), 4)

    def test_sharing_keeps_the_owner(self):
        db = DBMIN(8)
        db.start("Q1", {"A": (2, "lru")})
        db.start("Q2", {"B": (2, "lru")})
        self.assertFalse(db.request("Q1", "A", 5))
        self.assertTrue(db.request("Q2", "B", 5))
        self.assertEqual(db.owner[5], ("Q1", "A"))
        self.assertEqual(db.sets[("Q2", "B")].size, 0)
        self.assertEqual(db.reads, 1)
        db.finish("Q1")
        self.assertIsNone(db.owner[5])
        self.assertTrue(db.request("Q2", "B", 5))   # found on the free list, no read
        self.assertEqual(db.owner[5], ("Q2", "B"))
        self.assertEqual(db.reads, 1)
        db.check()

    def test_sets_behave_as_standalone_caches(self):
        # Without sharing, each locality set holds what a cache of its own size would hold,
        # and the free list can only save reads.
        for seed in range(25):
            rng = random.Random(seed)
            k = rng.randrange(1, 4)
            sets = {}
            for j in range(k):
                sets[j] = (rng.randrange(1, 5), rng.choice(["lru", "mru", "fifo"]))
            n_frames = sum(l for l, _ in sets.values()) + rng.randrange(1, 4)
            db = DBMIN(n_frames)
            self.assertTrue(db.start("Q", sets))
            traces = {j: [] for j in sets}
            trace = []
            for _ in range(300):
                j = rng.randrange(k)
                p = 100 * j + (rng.randrange(8) if rng.random() < 0.5 else rng.randrange(3))
                trace.append(((("Q", j)), p))
                traces[j].append(p)
                db.request("Q", j, p)
                db.check()
            plain_misses = 0
            for j, (l, policy) in sets.items():
                states = plain_cache(traces[j], l, policy)
                self.assertEqual(sorted(db.sets[("Q", j)].pages), states[-1])
                before = [[]] + states[:-1]
                plain_misses += sum(1 for p, s in zip(traces[j], before) if p not in s)
            self.assertLessEqual(db.reads, plain_misses)
            self.assertEqual(db.reads, reference_model(
                n_frames, {("Q", j): v for j, v in sets.items()}, trace))

    def test_random_with_sharing_and_admission(self):
        for seed in range(25):
            rng = random.Random(500 + seed)
            n_frames = rng.randrange(4, 12)
            db = DBMIN(n_frames)
            running = []
            for step in range(400):
                if rng.random() < 0.05 or not running:
                    q = f"Q{step}"
                    files = {f: (rng.randrange(1, max(2, n_frames // 2)), rng.choice(["lru", "mru", "fifo"]))
                             for f in range(rng.randrange(1, 3))}
                    if db.start(q, files):
                        running.append(q)
                elif rng.random() < 0.05:
                    q = running.pop(rng.randrange(len(running)))
                    running.extend(db.finish(q))
                else:
                    q = rng.choice(running)
                    f = rng.choice(db.active[q])
                    reads = db.reads
                    p = rng.randrange(20)
                    p_resident = p in db.owner
                    hit = db.request(q, f, p)
                    self.assertEqual(hit, p_resident)
                    self.assertEqual(db.reads - reads, 0 if hit else 1)
                    self.assertIn(p, db.owner)
                db.check()
                self.assertEqual(sorted(running), sorted(db.active))


if __name__ == "__main__":
    unittest.main()
