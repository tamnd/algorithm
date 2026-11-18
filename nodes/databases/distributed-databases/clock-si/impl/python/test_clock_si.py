# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-si/. The authors are listed in prov/9E7PE4.jsonl.
import itertools
import random
import unittest

from clock_si import ClockSI, Txn

PLACE = {"a0": 0, "a1": 0, "b0": 1, "b1": 1, "c0": 2, "c1": 2}
KEYS = sorted(PLACE)
INIT = {k: 10 * i for i, k in enumerate(KEYS)}


def workload(rng):
    txns = []
    for tid in range(1, rng.randint(3, 6) + 1):
        reads = rng.sample(KEYS, rng.randint(1, 3))
        writes = rng.sample(KEYS, rng.randint(1, 3)) if rng.random() < 0.7 else []
        txns.append(Txn(tid, rng.randrange(3), reads, writes, rng.randrange(10)))
    return txns


def make(rng, **kw):
    skews = [rng.randint(-3, 3) for _ in range(3)]
    return ClockSI(PLACE, skews, INIT, rng, **kw)


def violations(db, txns):
    """The brute force oracle for snapshot isolation. It knows only the
    committed writers and their timestamps, and lists every rule that the
    run breaks."""
    bad = []
    writers = [t for t in txns if t.status == "committed" and t.writes]

    def value_at(k, ts):
        ws = [w for w in writers if k in w.writes and w.commit < ts]
        return max(ws, key=lambda w: w.commit).writes[k] if ws else INIT[k]

    for t in txns:
        if len(t.reads) == len(t.read_keys):
            for k, v in t.reads.items():
                if v != value_at(k, t.snapshot):
                    bad.append(("read", t.tid, k))
    for a, b in itertools.combinations(writers, 2):
        if set(a.writes) & set(b.writes) and not (a.commit < b.snapshot or b.commit < a.snapshot):
            bad.append(("write-write", a.tid, b.tid))
    for w in writers:
        if not w.commit > w.snapshot:
            bad.append(("commit before snapshot", w.tid))
    if db.state() != {k: value_at(k, float("inf")) for k in KEYS}:
        bad.append(("final state",))
    for k in KEYS:                       # only committed writers left versions, nothing is pending
        if {tid for _, _, tid in db.versions[k]} != {0} | {w.tid for w in writers if k in w.writes}:
            bad.append(("versions", k))
        if db.pending[k]:
            bad.append(("pending", k))
    return bad


class TestClockSI(unittest.TestCase):
    def test_snapshot_isolation(self):
        stats = {"commit": 0, "abort": 0, "clock": 0, "pending": 0}
        for seed in range(300):
            rng = random.Random(seed)
            db = make(rng)
            txns = workload(rng)
            db.run(txns)
            self.assertEqual(violations(db, txns), [], seed)
            stats["commit"] += sum(t.status == "committed" and bool(t.writes) for t in txns)
            stats["abort"] += sum(t.status == "aborted" for t in txns)
            stats["clock"] += db.delays["clock"]
            stats["pending"] += db.delays["pending"]
        self.assertGreater(stats["abort"], 20)
        self.assertGreater(stats["clock"], 20)
        self.assertGreater(stats["pending"], 20)

    def test_coordinator_crash(self):
        for seed in range(200):
            rng = random.Random(1000 + seed)
            db = make(rng)
            txns = workload(rng)
            victim = rng.choice(txns).tid
            db.run(txns, crash=(victim, "prepare" if seed % 2 else "decided"))
            self.assertEqual(violations(db, txns), [], seed)

    def test_each_rule_is_needed(self):
        for flag in ("clock", "pending", "max"):
            broken = 0
            for seed in range(300):
                rng = random.Random(seed)
                db = make(rng, checks={flag: False})
                txns = workload(rng)
                db.run(txns)
                broken += bool(violations(db, txns))
            self.assertGreater(broken, 0, flag)

    def test_older_snapshots_wait_less(self):
        delays = []
        for delta in (0, 6):
            total = 0
            for seed in range(200):
                rng = random.Random(seed)
                db = make(rng, delta=delta)
                txns = workload(rng)
                db.run(txns)
                self.assertEqual(violations(db, txns), [])
                total += db.delays["clock"] + db.delays["pending"]
            delays.append(total)
        self.assertLess(delays[1], delays[0] / 2)

    def test_messages(self):
        # A read-only transaction with r remote reads sends 2 r messages; a
        # distributed commit over p remote participants sends 3 p more. No
        # message goes to a timestamp server.
        for r in range(4):
            for parts in ([1], [1, 2]):
                db = ClockSI(PLACE, [0, 0, 0], INIT, random.Random(0))
                reads = ["b0", "c0", "b1"][:r]
                writes = ["b0", "c0"][:len(parts)]
                t = Txn(1, 0, reads, writes, 0)
                db.run([t])
                self.assertEqual(t.status, "committed")
                commit = 2 if len(parts) == 1 else 3 * len(parts)
                self.assertEqual(db.messages, 2 * r + commit)

    def test_clock_skew_delay(self):
        # P0 is 5 ticks ahead of P1. T1 starts at P0 at tick 0 and reads b0
        # on P1; the read arrives by tick 2 and waits until P1's clock passes
        # the snapshot. T2 commits b0 on P1 at tick 3 with a smaller
        # timestamp, so T1 must see it.
        db = ClockSI(PLACE, [5, 0, 0], INIT, random.Random(0))
        t1 = Txn(1, 0, ["b0"], [], 0)
        t2 = Txn(2, 1, [], ["b0"], 3)
        db.run([t1, t2])
        self.assertEqual((t1.snapshot, t2.snapshot, t2.commit), (5000, 3001, 3011))
        self.assertEqual(t1.reads["b0"], t2.writes["b0"])
        self.assertEqual(db.delays["clock"], 1)
        db = ClockSI(PLACE, [5, 0, 0], INIT, random.Random(0), checks={"clock": False})
        t1, t2 = Txn(1, 0, ["b0"], [], 0), Txn(2, 1, [], ["b0"], 3)
        db.run([t1, t2])
        self.assertEqual(violations(db, [t1, t2]), [("read", 1, "b0")])


if __name__ == "__main__":
    unittest.main()
