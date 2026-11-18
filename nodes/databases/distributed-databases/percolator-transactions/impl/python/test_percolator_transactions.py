# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/percolator-transactions/. The authors are listed in prov/FVBYZN.jsonl.
import itertools
import random
import unittest

from percolator_transactions import Table, Txn

INIT = {"a": 0, "b": 10, "c": 20, "d": 30}
KEYS = sorted(INIT)


def make_logic(tid, writes):
    return lambda vals: {k: sum(vals.values()) + 100 * tid + i for i, k in enumerate(writes)}


def workload(rng):
    txns = []
    for tid in range(1, rng.randint(3, 5) + 1):
        reads = rng.sample(KEYS, rng.randint(1, 3))
        writes = rng.sample(KEYS, rng.randint(1, 2)) if rng.random() < 0.8 else []
        txns.append(Txn(tid, reads, make_logic(tid, writes) if writes else None))
    return txns


def drive(table, txns, order):
    """Advance the clients in the given order of tids, then finish them."""
    gens = {t.tid: table.steps(t) for t in txns}
    for tid in order + sorted(gens) * 50:
        if tid in gens:
            try:
                next(gens[tid])
            except StopIteration:
                del gens[tid]
    return gens


class TestPercolator(unittest.TestCase):
    def check_si(self, table, txns, rng):
        """The brute force oracle. It computes from the committed writers
        alone what each read and the final state must be under snapshot
        isolation, and compares."""
        writers = [table.loader] + [t for t in txns if t.writes and table.is_committed(t)]

        def value_at(x, ts):
            ws = [w for w in writers if x in w.writes and w.commit < ts]
            return max(ws, key=lambda w: w.commit).writes[x]

        for t in txns:
            if len(t.reads) == len(t.read_keys):          # every read that returned
                for x, v in t.reads.items():
                    self.assertEqual(v, value_at(x, t.start), (t.tid, x))
        for a, b in itertools.combinations(writers, 2):   # first committer wins
            if set(a.writes) & set(b.writes):
                self.assertTrue(a.commit < b.start or b.commit < a.start, (a.tid, b.tid))
        for w in writers[1:]:
            self.assertEqual(w.writes, w.logic(dict(w.reads)))
        final = table.snapshot(rng)
        self.assertEqual(final, {x: value_at(x, table.ts + 1) for x in KEYS})
        for c in table.cells.values():                    # cleanup left nothing behind
            self.assertEqual(c.lock, {})
        committed = {w.start for w in writers}
        for x, c in table.cells.items():                  # atomic: all or nothing
            self.assertEqual(set(c.data), {s for s in committed if x in table.owner.get(s, table.loader).writes})
            for w in writers:
                if x in w.writes:
                    self.assertEqual(c.write.get(w.commit), w.start)
        return len(writers) - 1

    def test_snapshot_isolation_without_crashes(self):
        aborts = commits = 0
        for seed in range(300):
            rng = random.Random(seed)
            table = Table(INIT, rng)
            txns = workload(rng)
            table.run(rng, txns)
            commits += self.check_si(table, txns, rng)
            aborts += sum(1 for t in txns if t.status == "aborted")
            self.assertEqual(table.rolled_back + table.rolled_forward, 0)
        self.assertGreater(aborts, 30)
        self.assertGreater(commits, 300)

    def test_crashes_and_lazy_cleanup(self):
        forward = back = 0
        for seed in range(300):
            rng = random.Random(1000 + seed)
            table = Table(INIT, rng)
            txns = workload(rng)
            when = rng.randrange(25) if seed % 2 else "commit point"
            table.run(rng, txns, crash=(when, rng.randint(1, len(txns))))
            self.check_si(table, txns, rng)
            forward += table.rolled_forward
            back += table.rolled_back
        self.assertGreater(forward, 20)
        self.assertGreater(back, 10)

    def test_wrong_suspicion_is_safe(self):
        cleaned = 0
        for seed in range(200):
            rng = random.Random(5000 + seed)
            table = Table(INIT, rng, suspect=0.3)
            txns = workload(rng)
            table.run(rng, txns, crash=(rng.randrange(25), rng.randint(1, len(txns))))
            self.check_si(table, txns, rng)
            cleaned += sum(1 for t in txns if t.abort_reason == "cleaned up")
        self.assertGreater(cleaned, 5)

    def test_lost_update_is_prevented(self):
        rng = random.Random(0)
        table = Table(INIT, rng)
        t1 = Txn(1, ["a"], lambda v: {"a": v["a"] + 1})
        t2 = Txn(2, ["a"], lambda v: {"a": v["a"] + 1})
        drive(table, [t1, t2], [1, 2, 1, 2, 1, 2])        # both read a = 0, T1 locks a first
        self.assertEqual((t1.status, t2.status, t2.abort_reason), ("done", "aborted", "conflict"))
        self.assertEqual(table.snapshot(rng)["a"], 1)

    def test_write_skew_is_allowed(self):
        # The rule is x + y >= 1. Each transaction checks it in its snapshot
        # and sets one of the two to 0. Snapshot isolation commits both.
        init = {"x": 1, "y": 1}
        rng = random.Random(0)
        table = Table(init, rng)

        def guard(key):
            return lambda v: {key: 0} if v["x"] + v["y"] >= 2 else {}
        t1, t2 = Txn(1, ["x", "y"], guard("x")), Txn(2, ["x", "y"], guard("y"))
        drive(table, [t1, t2], [1, 2, 1, 1, 2, 2])
        self.assertEqual((t1.status, t2.status), ("done", "done"))
        final = table.snapshot(rng)
        self.assertEqual(final, {"x": 0, "y": 0})
        for order in itertools.permutations([guard("x"), guard("y")]):    # no serial order gives this
            s = dict(init)
            for logic in order:
                s.update(logic(dict(s)))
            self.assertNotEqual(s, final)

    def test_roll_forward_and_roll_back(self):
        for crash_after, want, forward, back in [(5, {"a": 5, "b": 6}, 1, 0), (4, {"a": 0, "b": 10}, 0, 2)]:
            rng = random.Random(0)
            table = Table(INIT, rng)
            t1 = Txn(1, [], lambda v: {"a": 5, "b": 6})
            gen = table.steps(t1)
            for _ in range(crash_after):     # 5 steps end at the commit point, 4 just before it
                next(gen)
            table.crashed.add(1)
            t2 = Txn(2, ["a", "b"], None)
            table.run(rng, [t2])
            self.assertEqual(t2.reads, want)
            self.assertEqual((table.rolled_forward, table.rolled_back), (forward, back))
            self.check_si(table, [t1, t2], rng)

    def test_requests_of_a_transaction_alone(self):
        rng = random.Random(0)
        for r in range(4):
            for w in range(1, 4):
                table = Table(INIT, rng)
                t = Txn(1, KEYS[:r], make_logic(1, KEYS[:w]))
                table.run(rng, [t])
                self.assertEqual(table.rpcs, r + 2 * w + 2)


if __name__ == "__main__":
    unittest.main()
