# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-one-write-all/. The authors are listed in prov/JG3SB7.jsonl.
import itertools
import random
import unittest

import dbsched
from read_one_write_all import ReplicatedDB

PLACEMENT = {"x": ["A", "B"], "y": ["B", "C"], "z": ["A", "C"]}


def one_copy_order(db):
    """A serial one-copy order equivalent to the physical history, by the
    definition of Bernstein, Hadzilacos and Goodman (Section 8.3): the same
    reads-from relation on items, and each final write of the one-copy
    history is a final write on some copy. None if there is no such order."""
    cp = dbsched.committed_projection(tuple(db.history))
    item = lambda copy: copy.split("@")[0]
    phys_rf = {}
    for occ, src in dbsched.reads_from(cp).items():
        phys_rf[(occ[0], item(occ[2]))] = None if src is None else src[0]
    finals = {(occ[0], item(c)) for c, occ in dbsched.final_writes(cp).items()}
    txns = sorted(dbsched.committed(cp))
    assert len(txns) <= dbsched.MAX_BRUTE_FORCE
    for order in itertools.permutations(txns):
        serial = tuple((k, t, x) for t in order for k, x in db.txns[t].ops)
        rf = {(occ[0], occ[2]): None if src is None else src[0]
              for occ, src in dbsched.reads_from(serial).items()}
        fw = dbsched.final_writes(serial)
        if rf == phys_rf and all((occ[0], x) in finals for x, occ in fw.items()):
            return order
    return None


def random_txns(rng, n):
    txns = {}
    for tid in range(1, n + 1):
        ops = []
        for x in rng.sample(sorted(PLACEMENT), rng.randint(1, 2)):
            ops += [(k, x) for k in rng.choice([["r"], ["w"], ["r", "w"]])]
        txns[tid] = ops
    return txns


def copies_agree(db):
    for x, sites in PLACEMENT.items():
        vals = {db.sites[s].value[x] for s in sites
                if db.sites[s].up and x in db.sites[s].readable}
        if len(vals) > 1:
            return False
    return True


class TestRowa(unittest.TestCase):
    def test_no_failures_one_copy_serializable(self):
        for seed in range(150):
            rng = random.Random(seed)
            db = ReplicatedDB(PLACEMENT, mode="rowa")
            db.run(rng, random_txns(rng, rng.randint(2, 4)))
            self.assertIsNotNone(one_copy_order(db), seed)
            self.assertTrue(copies_agree(db), seed)

    def test_all_short_pairs_commit_alone(self):
        # Each transaction run alone commits, and all copies get its writes.
        rng = random.Random(7)
        for tid, ops in random_txns(rng, 6).items():
            db = ReplicatedDB(PLACEMENT, mode="rowa")
            db.run(random.Random(tid), {tid: ops})
            self.assertEqual(db.txns[tid].status, "committed")
            self.assertTrue(copies_agree(db))

    def test_available_copies_with_failures(self):
        for seed in range(250):
            rng = random.Random(seed)
            db = ReplicatedDB(PLACEMENT, mode="available")
            site = rng.choice(["A", "B", "C"])
            t_fail = rng.randrange(6)
            events = [(t_fail, "fail", site), (t_fail + rng.randrange(1, 8), "recover", site)]
            db.run(rng, random_txns(rng, 3), events)
            self.assertIsNotNone(one_copy_order(db), seed)
            self.assertTrue(copies_agree(db), seed)

    def test_copier_that_writes_only_the_new_copy_is_wrong(self):
        # Seed 0 of the test above: a copier reads x@A and writes only x@B
        # while T3 holds a shared lock on x@A; the result is not 1SR.
        bad = 0
        for seed in range(40):
            rng = random.Random(seed)
            db = ReplicatedDB(PLACEMENT, mode="available", copier_writes_all=False)
            site = rng.choice(["A", "B", "C"])
            t_fail = rng.randrange(6)
            events = [(t_fail, "fail", site), (t_fail + rng.randrange(1, 8), "recover", site)]
            db.run(rng, random_txns(rng, 3), events)
            bad += one_copy_order(db) is None
        self.assertGreater(bad, 0)

    def test_plain_rowa_aborts_a_write_when_a_copy_is_down(self):
        db = ReplicatedDB(PLACEMENT, mode="rowa")
        db.fail("B")
        db.run(random.Random(1), {1: [("r", "x")], 2: [("w", "y")], 3: [("w", "z")]})
        self.assertEqual(db.txns[1].status, "committed")   # reads copy at A
        self.assertEqual(db.txns[2].status, "aborted")     # y@B is down
        self.assertEqual(db.txns[3].status, "committed")   # z is on A and C

    def test_available_copies_write_skips_a_down_copy(self):
        db = ReplicatedDB(PLACEMENT, mode="available")
        db.fail("B")
        db.run(random.Random(1), {2: [("w", "y")]})
        self.assertEqual(db.txns[2].status, "committed")
        self.assertEqual(db.sites["C"].value["y"], 200)

    def bhg_example(self, mode):
        # T1 = r1[x] w1[y], T2 = r2[y] w2[x]. T1 reads x@A, T2 reads y@C,
        # then A and C fail, so each write misses one copy.
        db = ReplicatedDB({"x": ["A", "B"], "y": ["C", "D"]}, mode=mode)
        db.start(1, [("r", "x"), ("w", "y")])
        db.start(2, [("r", "y"), ("w", "x")])
        while len([a for a in db.history if a[0] == "r"]) < 2:
            db.deliver(0)
        while db.net and db.net[0][0][0] == "txn":
            db.deliver(0)
        db.fail("A")
        db.fail("C")
        while db.net:
            db.deliver(0)
        return db

    def test_naive_write_all_available_is_not_1sr(self):
        db = self.bhg_example("naive")
        self.assertEqual(db.txns[1].status, "committed")
        self.assertEqual(db.txns[2].status, "committed")
        self.assertEqual(dbsched.format(db.history).count("r"), 2)
        self.assertIsNone(one_copy_order(db))
        # The copy-level history itself is conflict serializable.
        self.assertTrue(dbsched.is_conflict_serializable(tuple(
            (k, t, None if c is None else c.replace("@", "_")) for k, t, c in db.history)))

    def test_validation_rejects_the_bhg_example(self):
        db = self.bhg_example("available")
        self.assertEqual(db.txns[1].status, "aborted")
        self.assertEqual(db.txns[2].status, "aborted")
        self.assertIsNotNone(one_copy_order(db))

    def test_message_count(self):
        # A read costs one round trip, a write to k copies costs k round trips.
        db = ReplicatedDB({"x": ["A", "B"], "y": ["A", "B", "C"]}, mode="rowa")
        db.run(random.Random(3), {1: [("r", "x"), ("w", "y")]})
        self.assertEqual(db.messages, 2 * 1 + 2 * 3)

    def test_deadlock_is_broken(self):
        # Two transactions read x, then both write x: each waits for the
        # shared lock of the other on the copy they both read.
        found = False
        for seed in range(60):
            db = ReplicatedDB({"x": ["A", "B"]}, mode="rowa")
            db.run(random.Random(seed), {1: [("r", "x"), ("w", "x")],
                                         2: [("r", "x"), ("w", "x")]}, start_spread=1)
            self.assertIsNotNone(one_copy_order(db))
            for victim, cycle in db.victims:
                found = True
                self.assertEqual(victim, max(cycle))
        self.assertTrue(found)

    def test_helper_self_test(self):
        self.assertTrue(dbsched._self_test())


if __name__ == "__main__":
    unittest.main()
