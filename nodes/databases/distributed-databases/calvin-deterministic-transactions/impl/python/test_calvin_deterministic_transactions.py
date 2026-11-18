# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/calvin-deterministic-transactions/. The authors are listed in prov/AX20CH.jsonl.
import random
import unittest

from calvin_deterministic_transactions import RESTART, Calvin, Txn, serial

PLACE = {"a0": 0, "a1": 0, "b0": 1, "b1": 1, "c0": 2, "c1": 2}
KEYS = sorted(PLACE)


def make_logic(tid, writes):
    def logic(vals):
        s = sum(vals.values())
        if s % 7 == 3:
            return None                  # a deterministic abort, such as "stock below zero"
        return {k: s + tid for k in writes}
    return logic


def workload(rng):
    reqs = []
    for tid in range(1, rng.randint(3, 6) + 1):
        reads = rng.sample(KEYS, rng.randint(0, 3))
        writes = rng.sample(KEYS, rng.randint(1, 2))
        reqs.append((rng.randrange(3), rng.randrange(3), Txn(tid, reads, writes, make_logic(tid, writes))))
    return reqs


def expected_read_messages(db, order):
    """Phase 3 messages per replica: each partition with reads sends to each
    other active participant."""
    return sum(len(db.active(t) - {s}) for t in order for s in db.read_parts(t))


def dependent(tid, read):
    """OLLP: the reconnaissance read of the index i predicts which account
    the transaction will change."""
    j = read("i")
    key = "b%d" % j

    def logic(vals):
        if vals["i"] != j:
            return RESTART               # the prediction is out of date
        return {key: vals[key] + 1}
    return Txn(tid, {"i", key}, {key}, logic)


class TestCalvin(unittest.TestCase):
    def check_run(self, db, reqs, r):
        order = db.global_order()
        want_state, want_results = serial(db.init, order)
        self.assertEqual(db.state(r), want_state)
        self.assertEqual(db.results(r), want_results)
        for (rr, q), s in db.sched.items():
            if rr == r:                  # no transaction is stuck at any partition
                self.assertEqual(s.finished, {t.tid for t in order if q in db.parts(t)})

    def test_every_replica_equals_the_serial_order(self):
        aborts = 0
        for seed in range(300):
            rng = random.Random(seed)
            db = Calvin(PLACE, replicas=2)
            reqs = workload(rng)
            db.run(rng, reqs)
            self.assertEqual(len(db.global_order()), len(reqs))
            for r in range(2):
                self.check_run(db, reqs, r)
            self.assertEqual(db.read_messages, 2 * expected_read_messages(db, db.global_order()))
            aborts += sum(1 for o, _ in db.results(0).values() if o == "abort")
        self.assertGreater(aborts, 10)

    def test_the_order_is_epoch_then_sequencer(self):
        db = Calvin(PLACE, replicas=1)
        t = [Txn(i, [], ["a0"], (lambda i: lambda v: {"a0": i})(i)) for i in range(4)]
        db.run(random.Random(0), [(1, 0, t[0]), (0, 2, t[1]), (0, 1, t[2]), (1, 0, t[3])])
        self.assertEqual([x.tid for x in db.global_order()], [2, 1, 0, 3])
        self.assertEqual(db.state(0)["a0"], 3)

    def test_crossing_transactions_never_deadlock(self):
        # T1 and T2 lock a0 and b0 in different program orders. The locks
        # are requested in the global order at each partition, so a later
        # transaction only waits for an earlier one.
        for seed in range(200):
            rng = random.Random(seed)
            db = Calvin(PLACE, replicas=1)
            t1 = Txn(1, ["a0", "b0"], ["a0", "b0"], lambda v: {"a0": v["b0"] + 1, "b0": v["a0"] + 1})
            t2 = Txn(2, ["b0", "a0"], ["b0", "a0"], lambda v: {"b0": v["a0"] * 2, "a0": v["b0"] * 2})
            db.run(rng, [(0, rng.randrange(3), t1), (0, rng.randrange(3), t2)])
            self.check_run(db, None, 0)

    def test_deterministic_abort_needs_no_vote(self):
        # Both active participants see the same values and abort alone.
        db = Calvin(PLACE, replicas=2, init={"a0": 5, "b0": 0})
        t = Txn(1, ["a0", "b0"], ["a0", "b0"],
                lambda v: None if v["a0"] < 10 else {"a0": v["a0"] - 10, "b0": v["b0"] + 10})
        db.run(random.Random(1), [(0, 0, t)])
        for r in range(2):
            self.assertEqual((db.state(r)["a0"], db.state(r)["b0"]), (5, 0))
            self.assertEqual(db.results(r)[1][0], "abort")
        self.assertEqual(db.read_messages, 2 * 2)     # a0 to P1 and b0 to P0, in each replica

    def test_crash_and_replay_of_the_input_log(self):
        replayed = 0
        for seed in range(150):
            rng = random.Random(seed)
            db = Calvin(PLACE, replicas=2)
            reqs = workload(rng)
            db.run(rng, reqs, crash=(rng.randrange(3), 1))
            self.check_run(db, reqs, 0)            # replica 0 did not wait for replica 1
            if db.state(1) != db.state(0):
                replayed += 1
            db.recover(1)
            db.drain(rng)
            self.check_run(db, reqs, 1)
        self.assertGreater(replayed, 50)

    def test_ollp_restart(self):
        place = {"i": 0, "b0": 1, "b1": 1}
        for seed in range(50):
            rng = random.Random(seed)
            db = Calvin(place, replicas=2)
            t1 = Txn(1, [], ["i"], lambda v: {"i": 1})     # moves the index to b1
            t2 = dependent(2, db.read_no_lock)              # predicts b0
            db.recon[2] = dependent
            db.run(rng, [(0, 0, t1), (0, 1, t2)])
            order = db.global_order()
            self.assertEqual([t.tid for t in order], [1, 2, 1001])
            for r in range(2):
                self.assertEqual(db.results(r)[2][0], RESTART)
                self.assertEqual(db.results(r)[1001][0], "commit")
                self.assertEqual(db.state(r), {"i": 1, "b0": 0, "b1": 1})
                self.check_run(db, None, r)


if __name__ == "__main__":
    unittest.main()
