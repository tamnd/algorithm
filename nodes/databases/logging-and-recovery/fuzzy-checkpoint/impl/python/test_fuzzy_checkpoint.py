# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fuzzy-checkpoint/. The authors are listed in prov/EF79FV.jsonl.

"""Crash-injection tests for fuzzy checkpoints with tables copied at different
times.

A seeded generator builds a strict workload against a live database: page
locks are held until the END record, commits are forced, aborts roll back one
CLR at a time, page writes (steals) and log flushes come at random places, and
the steps of each checkpoint (begin, the two copies in a random order, end) are
spread among the other steps. Each test replays a prefix, crashes, recovers and
compares the result with the oracle: the writes of the committed transactions,
applied in commit order.
"""

import copy
import random
import unittest

from fuzzy_checkpoint import Db

PAGES = "pqrst"
INIT = {p: 0 for p in PAGES}


def make_workload(db: Db, rng: random.Random, n_ops: int, first_txn: int = 1) -> list:
    ops: list = []
    owner: dict[str, int] = {}
    state: dict[int, str] = {}  # txn -> active, committed or aborting
    next_txn, next_val = first_txn, 100 * first_txn
    ck: list = []  # the checkpoint steps still to do
    while len(ops) < n_ops:
        roll = rng.random()
        active = [t for t, s in state.items() if s == "active"]
        if roll < 0.10 and len(state) < 4:
            op = ("begin", next_txn)
            state[next_txn] = "active"
            next_txn += 1
        elif roll < 0.42 and active:
            t = rng.choice(active)
            free = [p for p in PAGES if owner.get(p, t) == t]
            if not free:
                continue
            next_val += 1
            op = ("update", t, rng.choice(free), next_val)
            owner[op[2]] = t
        elif roll < 0.52 and active:
            t = rng.choice(active)
            if rng.random() < 0.7:
                op = ("commit", t)
                state[t] = "committed"
            else:
                op = ("abort", t)
                state[t] = "aborting"
        elif roll < 0.64 and len(state) > len(active):
            t = rng.choice(sorted(t for t in state if state[t] != "active"))
            op = ("end", t) if state[t] == "committed" else ("undo_step", t)
        elif roll < 0.76 and db.buf:
            op = ("flush_page", rng.choice(sorted(db.buf)))
        elif roll < 0.80:
            op = ("flush_log",)
        elif roll < 0.92:
            if not ck:
                ck = ["copy_att", "copy_dpt"]
                rng.shuffle(ck)
                ck = ["ckpt_begin"] + ck + ["ckpt_end"]
            op = (ck.pop(0),)
        else:
            continue
        done = apply_op(db, op)
        if done or op[0] == "end":
            del state[op[1]]
            owner = {p: u for p, u in owner.items() if u != op[1]}
        ops.append(op)
    return ops


def apply_op(db: Db, op: tuple):
    return getattr(db, op[0])(*op[1:])


def oracle(base: dict, ops: list) -> dict:
    state = dict(base)
    pending: dict[int, list] = {}
    for op in ops:
        if op[0] == "begin":
            pending[op[1]] = []
        elif op[0] == "update":
            pending[op[1]].append((op[2], op[3]))
        elif op[0] == "commit":
            for p, w in pending[op[1]]:
                state[p] = w
    return state


def replay(snap: tuple, ops: list) -> Db:
    db = Db(dict(snap[0]), list(snap[1]), snap[2])
    for op in ops:
        apply_op(db, op)
    return db


def snapshot(db: Db) -> tuple:
    return dict(db.disk), list(db.log), db.master


def disk_state(db: Db) -> dict:
    return {p: v for p, (_, v) in sorted(db.disk.items())}


def recover_and_flush(db: Db) -> dict:
    db.recover()
    for p in sorted(db.buf):
        db.flush_page(p)
    return disk_state(db)


def losers(att: dict) -> dict:
    return {t: (e[1], e[2]) for t, e in att.items() if e[0] != "committed"}


class TestCrashInjection(unittest.TestCase):
    def test_crash_after_every_prefix(self):
        for seed in range(25):
            rng = random.Random(seed)
            ops = make_workload(Db(INIT), rng, 80)
            for k in range(len(ops) + 1):
                db = replay((INIT, [], 0), ops[:k]).crash()
                self.assertEqual(recover_and_flush(db), oracle(INIT, ops[:k]), (seed, k))

    def test_analysis_tables(self):
        # The merged tables cover every logged change missing from the disk,
        # and the losers agree with an analysis of the whole log.
        checked = 0
        for seed in range(25):
            rng = random.Random(500 + seed)
            ops = make_workload(Db(INIT), rng, 80)
            for k in range(len(ops) + 1):
                db = replay((INIT, [], 0), ops[:k]).crash()
                att, dpt, redo_lsn = db.analysis()
                for r in db.log:
                    if r.kind in ("UPDATE", "CLR") and r.lsn > db.disk[r.page][0]:
                        self.assertIn(r.page, dpt, (seed, k, r))
                        self.assertLessEqual(dpt[r.page], r.lsn, (seed, k, r))
                        self.assertLessEqual(redo_lsn, r.lsn)
                        checked += 1
                full_att, _, _ = db.analysis(start=1, use_checkpoints=False)
                self.assertEqual(losers(att), losers(full_att), (seed, k))
                self.assertEqual({t for t, e in att.items() if e[0] == "committed"}, {t for t, e in full_att.items() if e[0] == "committed"})
        self.assertGreater(checked, 1000)

    def test_crash_during_recovery(self):
        for seed in range(10):
            rng = random.Random(1000 + seed)
            ops = make_workload(Db(INIT), rng, 70)
            for k in range(0, len(ops) + 1, 3):
                want = oracle(INIT, ops[:k])
                for j in range(0, 30, 2):
                    db = replay((INIT, [], 0), ops[:k]).crash()
                    finished = False
                    for rounds in (j, j // 2):
                        steps = db.recovery()
                        for _ in range(rounds):
                            if next(steps, None) is None:
                                finished = True
                                break
                            x = rng.random()
                            if x < 0.4 and db.buf:
                                db.flush_page(rng.choice(sorted(db.buf)))
                            elif x < 0.6:
                                db.flush_log()
                        db = db.crash()
                    self.assertEqual(recover_and_flush(db), want, (seed, k, j))
                    if finished:
                        break

    def test_two_eras(self):
        for seed in range(10):
            rng = random.Random(2000 + seed)
            ops1 = make_workload(Db(INIT), rng, 60)
            cut = rng.randrange(len(ops1) + 1)
            db = replay((INIT, [], 0), ops1[:cut]).crash()
            db.recover()
            base = oracle(INIT, ops1[:cut])
            self.assertEqual(db.state(), base)
            # keep the dirty pages of recovery in the buffer, and go on
            ops2 = make_workload(copy.deepcopy(db), rng, 60, first_txn=1000)
            for k in range(len(ops2) + 1):
                live = copy.deepcopy(db)
                for op in ops2[:k]:
                    apply_op(live, op)
                got = recover_and_flush(live.crash())
                self.assertEqual(got, oracle(base, ops2[:k]), (seed, k))

    def test_aries_replace_rule_is_also_correct(self):
        # ARIES sets the recLSN to the copied value instead of the minimum.
        class Replace(Db):
            def merge_checkpoint(self, att, dpt, ended, r):
                for t, status, last, nxt in r.att:
                    if t not in att and t not in ended:
                        att[t] = [status, last, nxt]
                for p, rec_lsn in r.dpt:
                    dpt[p] = rec_lsn

            def crash(self):
                return Replace(dict(self.disk), list(self.log), self.master)

        for seed in range(20):
            rng = random.Random(3000 + seed)
            ops = make_workload(Db(INIT), rng, 80)
            for k in range(len(ops) + 1):
                db = Replace(dict(INIT))
                for op in ops[:k]:
                    apply_op(db, op)
                self.assertEqual(recover_and_flush(db.crash()), oracle(INIT, ops[:k]), (seed, k))


def page_example() -> Db:
    db = Db({"P": 10, "Q": 20, "R": 30})
    db.begin(1)
    db.update(1, "P", 11)
    db.begin(2)
    db.update(2, "Q", 21)
    db.ckpt_begin()
    db.copy_att()
    db.commit(1)
    db.end(1)
    db.update(2, "R", 31)
    db.flush_page("P")
    db.copy_dpt()
    db.ckpt_end()
    db.begin(3)
    db.update(3, "P", 12)
    db.commit(2)
    db.end(2)
    return db


class TestExampleAndPitfalls(unittest.TestCase):
    def test_page_example(self):
        db = page_example()
        self.assertEqual(db.master, 5)
        end = db.log[8]
        self.assertEqual(end.kind, "END_CHECKPOINT")
        self.assertEqual(end.att, ((1, "active", 2, 2), (2, "active", 4, 4)))
        self.assertEqual(end.dpt, (("Q", 4), ("R", 8)))
        db = db.crash()
        self.assertEqual(len(db.log), 12)
        self.assertEqual(db.disk, {"P": (2, 11), "Q": (0, 20), "R": (0, 30)})
        att, dpt, redo_lsn = db.analysis()
        self.assertEqual(att, {2: ["committed", 12, 8], 3: ["active", 11, 11]})
        self.assertEqual(dpt, {"Q": 4, "R": 8, "P": 11})
        self.assertEqual(redo_lsn, 4)
        db.recover()
        self.assertEqual(db.stats, {"analysis": 8, "redo": 9, "undo": 1, "page_reads": 3})
        self.assertEqual(db.state(), {"P": 11, "Q": 21, "R": 31})
        kinds = [(r.lsn, r.kind, r.txn) for r in db.log[12:]]
        self.assertEqual(kinds, [(13, "END", 2), (14, "CLR", 3), (15, "END", 3)])

    def test_readding_an_ended_transaction_is_wrong(self):
        class NoEnded(Db):
            def merge_checkpoint(self, att, dpt, ended, r):
                super().merge_checkpoint(att, dpt, set(), r)

        db = page_example().crash()
        bad = NoEnded(dict(db.disk), list(db.log), db.master)
        bad.recover()
        self.assertEqual(bad.state(), {"P": 10, "Q": 21, "R": 31})  # T1 was committed

    def test_redo_from_the_begin_record_is_wrong(self):
        class FromBegin(Db):
            def analysis(self, start=None, use_checkpoints=True):
                att, dpt, _ = super().analysis(start, use_checkpoints)
                return att, dpt, self.master

        db = page_example().crash()
        bad = FromBegin(dict(db.disk), list(db.log), db.master)
        bad.recover()
        self.assertEqual(bad.state()["Q"], 20)  # the committed write of T2 is lost

    def test_copy_before_the_begin_record_is_wrong(self):
        db = Db({"P": 10})
        db.copy_att()
        db.copy_dpt()
        early = dict(db.ck)
        db.begin(1)
        db.update(1, "P", 11)
        db.commit(1)
        db.end(1)
        db.ckpt_begin()
        db.ck.update(att=early["att"], dpt=early["dpt"])  # tables from before the begin record
        db.ckpt_end()
        db = db.crash()
        db.recover()
        self.assertEqual(db.state(), {"P": 10})  # the committed write is lost
        good = Db({"P": 10})
        good.begin(1)
        good.update(1, "P", 11)
        good.commit(1)
        good.end(1)
        good.ckpt_begin()
        good.copy_att()
        good.copy_dpt()
        good.ckpt_end()
        good = good.crash()
        good.recover()
        self.assertEqual(good.state(), {"P": 11})

    def test_master_before_the_force_is_wrong(self):
        class EarlyMaster(Db):
            def ckpt_end(self):
                self._append(kind="END_CHECKPOINT", att=self.ck["att"], dpt=self.ck["dpt"])
                self.master = self.ck["b"]  # set before the record is stable

        db = EarlyMaster({"P": 10})
        db.begin(1)
        db.update(1, "P", 11)
        db.commit(1)
        db.ckpt_begin()
        db.copy_att()
        db.copy_dpt()
        db.ckpt_end()
        db = db.crash()
        self.assertEqual(len(db.log), 3)
        self.assertEqual(db.master, 4)
        db.recover()
        self.assertEqual(db.state(), {"P": 10})  # the committed write is lost

    def test_checkpoint_bounds_analysis(self):
        def run(with_ckpt: bool) -> Db:
            db = Db(dict(INIT))
            rng = random.Random(9)
            for t in range(1, 51):
                db.begin(t)
                db.update(t, rng.choice(PAGES), t)
                db.commit(t)
                db.end(t)
                if t % 10 == 0:
                    for p in sorted(db.buf):
                        db.flush_page(p)
            db.begin(99)
            db.update(99, "p", -1)
            if with_ckpt:
                db.ckpt_begin()
                db.copy_att()
                db.copy_dpt()
                db.ckpt_end()
            db.update(99, "q", -2)
            db.flush_log()
            return db.crash()

        a, b = run(False), run(True)
        a.recover()
        b.recover()
        self.assertEqual(a.state(), b.state())
        self.assertEqual((a.stats["analysis"], b.stats["analysis"]), (203, 3))
        # without a checkpoint, analysis cannot know that the pages were written
        self.assertEqual((a.stats["redo"], b.stats["redo"]), (202, 4))


if __name__ == "__main__":
    unittest.main()
