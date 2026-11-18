# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ramp-transactions/. The authors are listed in prov/1YZCSM.jsonl.
import random
import unittest

from ramp_transactions import BOTTOM, RampDB

PLACEMENT = {"x": "P0", "y": "P1", "z": "P2", "w": "P0"}
KEYS = sorted(PLACEMENT)


def fractured(db):
    """The reads that break read atomicity (Bailis et al. 2014, Section 3.1):
    a reader sees the write of T to one key and an older version of another
    key that T also wrote. Also the reads of a version whose writer never
    finished its prepare round."""
    writes = {ts: set(keys) for ev, ts, keys in db.log if ev == "commit"}
    bad = []
    for ev, cid, got in db.log:
        if ev != "read":
            continue
        for x, t in got.items():
            if t == BOTTOM:
                continue
            if t not in writes:
                bad.append((cid, "uncommitted", x, t))
                continue
            for y in writes[t] & set(got):
                if got[y] < t:
                    bad.append((cid, "fractured", x, y, t, got[y]))
    return bad


def workload(rng, crash=False):
    ops, cid = [], 1
    for seq in range(1, rng.randint(2, 4) + 1):
        keys = rng.sample(KEYS, rng.randint(2, 3))
        ops.append((rng.randrange(12), "w", cid, seq, {k: 10 * seq + i for i, k in enumerate(keys)}))
        cid += 1
    for _ in range(rng.randint(2, 4)):
        ops.append((rng.randrange(16), "r", cid, rng.sample(KEYS, rng.randint(2, 4))))
        cid += 1
    crashes = []
    if crash:
        writers = [o[2] for o in ops if o[1] == "w"]
        crashes = [(rng.randrange(20), rng.choice(writers))]
    return ops, crashes


class TestRamp(unittest.TestCase):
    def check(self, mode, crash):
        reads = 0
        for seed in range(200):
            rng = random.Random(seed)
            db = RampDB(PLACEMENT, mode)
            ops, crashes = workload(rng, crash)
            db.run(rng, ops, crashes)
            self.assertEqual(fractured(db), [], (mode, seed))
            for c in db.clients.values():
                if hasattr(c, "keys"):
                    self.assertEqual(c.state, "done")              # no reader blocks
                    self.assertLessEqual(c.rounds, 2)
                    reads += 1
        self.assertGreater(reads, 400)

    def test_fast_is_read_atomic(self):
        self.check("fast", crash=False)

    def test_fast_with_writer_crashes(self):
        self.check("fast", crash=True)

    def test_small_is_read_atomic(self):
        self.check("small", crash=False)

    def test_small_with_writer_crashes(self):
        self.check("small", crash=True)

    def test_one_round_reads_are_not_atomic(self):
        bad = 0
        for seed in range(200):
            rng = random.Random(seed)
            db = RampDB(PLACEMENT, "naive")
            ops, crashes = workload(rng)
            db.run(rng, ops, crashes)
            bad += bool(fractured(db))
        self.assertGreater(bad, 0)

    def race(self, mode):
        """T1 writes x and y. The commit has reached x only when T1 crashes;
        then client 2 reads x and y."""
        db = RampDB(PLACEMENT, mode)
        db.put_all(1, 1, {"x": 11, "y": 12})
        while db.net:
            db.deliver(0)
            if db.clients[1].state == "committing":
                break
        k = next(i for i, m in enumerate(db.net) if m[1][0] == "commit" and m[1][2] == "x")
        db.deliver(k)
        db.crash(1)
        db.net = [m for m in db.net if m[1][0] != "commit"]   # the commit to y is lost with T1
        before = db.messages
        db.get_all(2, ["x", "y"])
        while db.net:
            db.deliver(0)
        return db, db.messages - before

    def test_second_round_repairs_a_race(self):
        db, msgs = self.race("fast")
        r = db.clients[2]
        self.assertEqual({k: r.ret[k][1] for k in r.ret}, {"x": 11, "y": 12})
        self.assertEqual((r.rounds, msgs), (2, 6))
        self.assertEqual(db.parts["P1"].last_commit["y"], BOTTOM)   # y is still not committed
        db, msgs = self.race("small")
        self.assertEqual({k: v[1] for k, v in db.clients[2].ret.items()}, {"x": 11, "y": 12})
        db, msgs = self.race("naive")
        self.assertEqual({k: v[1] for k, v in db.clients[2].ret.items()}, {"x": 11, "y": 0})
        self.assertTrue(fractured(db))

    def test_round_trips(self):
        # With no concurrent writer, RAMP-F reads in one round trip and
        # RAMP-S in two. A write takes two round trips in both.
        for mode, rounds in (("fast", 1), ("small", 2)):
            db = RampDB(PLACEMENT, mode)
            db.run(random.Random(0), [(0, "w", 1, 1, {"x": 11, "y": 12, "z": 13})])
            self.assertEqual((db.clients[1].rounds, db.messages), (2, 12))
            before = db.messages
            db.run(random.Random(0), [(0, "r", 2, ["x", "y", "z", "w"])])
            self.assertEqual(db.clients[2].rounds, rounds)
            self.assertEqual(db.messages - before, 8 * rounds)
            self.assertEqual({k: v[1] for k, v in db.clients[2].ret.items()},
                             {"x": 11, "y": 12, "z": 13, "w": 0})

    def test_metadata_size(self):
        # RAMP-F stores the other keys of the write set with each version,
        # RAMP-S nothing.
        for mode, size in (("fast", 2), ("small", 0)):
            db = RampDB(PLACEMENT, mode)
            db.run(random.Random(0), [(0, "w", 1, 1, {"x": 1, "y": 2, "z": 3})])
            self.assertEqual(len(db.parts["P0"].versions["x"][(1, 1)][1]), size)


if __name__ == "__main__":
    unittest.main()
