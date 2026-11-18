# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/undo-redo-logging/. The authors are listed in prov/E549PJ.jsonl.

"""Crash-injection tests for undo/redo logging.

A seeded generator builds a strict workload against a live database: write
locks are held to the end of each transaction, page outputs (steals), log
flushes, aborts and the three steps of a nonquiescent checkpoint come at random
places. Each test replays a prefix of the workload, crashes, recovers and
compares the result with the oracle: the writes of the committed transactions,
applied in commit order.
"""

import random
import unittest

from undo_redo_logging import Db, Rec

ITEMS = "abcde"


def make_workload(db: Db, rng: random.Random, n_ops: int, first_txn: int = 1) -> list:
    """Run n_ops random steps on db and return them as a list of tuples."""
    ops: list = []
    owner: dict[str, int] = {}  # item -> the transaction that holds its write lock
    active: list[int] = []
    next_txn = first_txn
    next_val = 100 * first_txn
    phase = 0  # 0: no checkpoint, 1: after START CKPT, 2: after the flush
    while len(ops) < n_ops:
        roll = rng.random()
        if roll < 0.12 and len(active) < 4:
            op = ("start", next_txn)
            active.append(next_txn)
            next_txn += 1
        elif roll < 0.55 and active:
            t = rng.choice(active)
            free = [x for x in ITEMS if owner.get(x, t) == t]
            if not free:
                continue
            x = rng.choice(free)
            next_val += 1
            op = ("write", t, x, next_val)
            owner[x] = t
        elif roll < 0.68 and active:
            t = rng.choice(active)
            op = ("commit", t) if rng.random() < 0.7 else ("abort", t)
            active.remove(t)
            owner = {x: u for x, u in owner.items() if u != t}
        elif roll < 0.80 and db.buf:
            op = ("output", rng.choice(sorted(db.buf)))
        elif roll < 0.86:
            op = ("flush",)
        elif roll < 0.95:
            op = ("ckpt_start", "ckpt_flush", "ckpt_end")[phase]
            op = (op,)
            phase = (phase + 1) % 3
        else:
            continue
        apply_op(db, op)
        ops.append(op)
    return ops


def apply_op(db: Db, op: tuple) -> None:
    kind = op[0]
    if kind == "start":
        db.start(op[1])
    elif kind == "write":
        db.write(op[1], op[2], op[3])
    elif kind == "commit":
        db.commit(op[1])
    elif kind == "abort":
        db.abort(op[1])
    elif kind == "output":
        db.output(op[1])
    elif kind == "flush":
        db.flush_log()
    else:
        getattr(db, kind)()


def oracle(base: dict, ops: list) -> dict:
    """The committed writes, applied in commit order, on top of base."""
    state = dict(base)
    pending: dict[int, list] = {}
    for op in ops:
        if op[0] == "start":
            pending[op[1]] = []
        elif op[0] == "write":
            pending[op[1]].append((op[2], op[3]))
        elif op[0] == "commit":
            for x, w in pending.pop(op[1]):
                state[x] = w
        elif op[0] == "abort":
            pending.pop(op[1])
    return state


def snapshot(db: Db) -> tuple:
    return dict(db.disk), list(db.log)


def replay(snap: tuple, ops: list) -> Db:
    db = Db(dict(snap[0]), list(snap[1]))
    for op in ops:
        apply_op(db, op)
    return db


def recover_with_crashes(db: Db, rng: random.Random, stop_after: int) -> tuple[Db, bool]:
    """Run recovery for stop_after steps with random outputs between steps,
    then crash. Return the crashed database and whether recovery finished."""
    steps = db.recovery()
    for _ in range(stop_after):
        if next(steps, None) is None:
            return db.crash(), True
        if db.buf and rng.random() < 0.5:
            db.output(rng.choice(sorted(db.buf)))
    return db.crash(), False


def recovered_state(db: Db) -> dict:
    db.recover()
    assert not db.buf and not db.tail
    return {x: v for x, (_, v) in sorted(db.disk.items())}


INIT = {x: 0 for x in ITEMS}


class TestCrashInjection(unittest.TestCase):
    def test_crash_after_every_prefix(self):
        for seed in range(25):
            rng = random.Random(seed)
            ops = make_workload(Db(INIT), rng, 70)
            for k in range(len(ops) + 1):
                db = replay((INIT, []), ops[:k]).crash()
                self.assertEqual(recovered_state(db), oracle(INIT, ops[:k]), (seed, k))

    def test_crash_during_recovery(self):
        for seed in range(12):
            rng = random.Random(1000 + seed)
            ops = make_workload(Db(INIT), rng, 60)
            for k in range(0, len(ops) + 1, 3):
                want = oracle(INIT, ops[:k])
                for j in range(0, 40, 2):
                    db = replay((INIT, []), ops[:k]).crash()
                    db, done = recover_with_crashes(db, rng, j)
                    # a second crash inside the second recovery
                    db, _ = recover_with_crashes(db, rng, j // 2)
                    self.assertEqual(recovered_state(db), want, (seed, k, j))
                    if done:
                        break

    def test_two_eras(self):
        # Recover, keep working on the recovered database, crash again.
        for seed in range(10):
            rng = random.Random(2000 + seed)
            ops1 = make_workload(Db(INIT), rng, 50)
            cut = rng.randrange(len(ops1) + 1)
            db = replay((INIT, []), ops1[:cut]).crash()
            base = recovered_state(db)
            self.assertEqual(base, oracle(INIT, ops1[:cut]))
            snap = snapshot(db)
            ops2 = make_workload(replay(snap, []), rng, 50, first_txn=1000)
            for k in range(len(ops2) + 1):
                db2 = replay(snap, ops2[:k]).crash()
                self.assertEqual(recovered_state(db2), oracle(base, ops2[:k]), (seed, k))


def page_example() -> Db:
    """The example of the page, built step by step."""
    db = Db({"A": 10, "B": 20, "C": 30})
    db.start(1)
    db.write(1, "A", 11)
    db.start(2)
    db.write(2, "B", 21)
    db.commit(1)
    db.ckpt_start()
    db.write(2, "C", 31)
    db.start(3)
    db.write(3, "A", 12)
    db.ckpt_flush()
    db.ckpt_end()
    db.commit(2)
    db.write(3, "B", 22)
    db.output("B")
    return db


def redo_first_recover(db: Db) -> None:
    """The wrong order: redo the committed transactions, then undo the rest."""
    s, listed = db.last_checkpoint()
    cand = set(listed) | {r.txn for r in db.log[s:] if r.kind == "START"}
    committed = {r.txn for r in db.log if r.kind == "COMMIT"}
    for r in db.log[s:]:
        if r.kind == "UPDATE" and r.txn in committed:
            db.buf[r.item] = [r.lsn, r.new]
    for r in reversed(db.log):
        if r.kind == "UPDATE" and r.txn in cand and r.txn not in committed:
            db.buf[r.item] = [r.lsn, r.old]
    for x in sorted(db.buf):
        db.output(x)


class TestExamplesAndPitfalls(unittest.TestCase):
    def test_page_example(self):
        db = page_example()
        self.assertEqual(len(db.log), 12)
        self.assertEqual(db.disk, {"A": (9, 12), "B": (12, 22), "C": (7, 31)})
        db = db.crash()
        self.assertEqual(db.last_checkpoint(), (6, (2,)))
        steps = list(db.recovery())
        self.assertEqual(steps, ["undo", "undo", "redo", "output", "output", "output", "abort records"])
        self.assertEqual(db.read_count, 16)  # 10 in the undo pass, 6 in the redo pass
        self.assertEqual(db.state(), {"A": 11, "B": 21, "C": 31})
        self.assertEqual(db.log[-1], Rec(13, "ABORT", 3))

    def test_redo_first_is_wrong(self):
        def build() -> Db:
            db = Db({"X": 1})
            db.start(1)
            db.write(1, "X", 2)
            db.abort(1)  # the rollback is done in the buffer and is not logged
            db.start(2)
            db.write(2, "X", 3)
            db.commit(2)
            return db.crash()

        good = build()
        good.recover()
        self.assertEqual(good.state(), {"X": 3})
        bad = build()
        redo_first_recover(bad)
        self.assertEqual(bad.state(), {"X": 1})

    def test_aborted_transaction_must_be_undone(self):
        # A stolen value of an aborted transaction stays on disk if recovery
        # treats <ABORT T> as complete.
        db = Db({"X": 1})
        db.start(1)
        db.write(1, "X", 2)
        db.output("X")
        db.abort(1)
        db.start(2)
        db.commit(2)
        db = db.crash()
        self.assertEqual(db.disk["X"], (2, 2))
        db.recover()
        self.assertEqual(db.state(), {"X": 1})

    def test_ur1_violation_breaks_recovery(self):
        class NoWal(Db):
            def output(self, x):
                if x in self.buf:
                    self.disk[x] = tuple(self.buf.pop(x))

            def crash(self):
                return NoWal(dict(self.disk), list(self.log))

        db = NoWal({"X": 1})
        db.start(1)
        db.write(1, "X", 2)
        db.output("X")
        db = db.crash()
        self.assertEqual(db.log, [])
        db.recover()
        self.assertEqual(db.state(), {"X": 2})  # wrong: T1 never committed

    def test_checkpoint_bounds_the_scan(self):
        def run(with_ckpt: bool) -> Db:
            db = Db({x: 0 for x in ITEMS})
            rng = random.Random(7)
            for t in range(1, 41):
                db.start(t)
                for _ in range(3):
                    db.write(t, rng.choice(ITEMS), rng.randrange(1000))
                db.commit(t)
            if with_ckpt:
                db.ckpt_start()
                db.ckpt_flush()
                db.ckpt_end()
            db.start(99)
            db.write(99, "a", -1)
            db.start(98)
            db.write(98, "b", -2)
            db.commit(98)
            return db.crash()

        a, b = run(False), run(True)
        a.recover()
        b.recover()
        self.assertEqual(a.state(), b.state())
        self.assertEqual(b.read_count, 13)  # the numbers given on the page
        self.assertEqual(a.read_count, 410)


if __name__ == "__main__":
    unittest.main()
