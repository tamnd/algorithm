# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-level-recovery/. The authors are listed in prov/7Q7BG3.jsonl.

"""Crash-injection tests for two-level recovery.

A seeded generator builds a workload against a live database: transactions
run ADD operations whose level 0 actions interleave with those of other
transactions, level 0 locks are released at the end of each operation, aborts
roll back one step at a time with compensations, and page writes (steal) and
log flushes come at random places. Each test replays a prefix, crashes,
recovers and compares the counters with the oracle: the initial values plus
the deltas of the transactions whose commit record is in the stable log.
"""

import copy
import random
from collections import Counter

from multi_level_recovery import INIT, MLR, fresh_disk

KEYS = ["a", "b", "c", "d"]
PAGES = ["P0", "P1", "P2"]


def apply(db: MLR, op: tuple) -> None:
    kind = op[0]
    if kind == "begin":
        db.begin(op[1])
    elif kind == "add":
        db.add(op[1], op[2], op[3])
    elif kind == "step":
        db.step(op[1])
    elif kind == "commit":
        db.commit(op[1])
    elif kind == "abort":
        db.abort(op[1])
    elif kind == "flush":
        db.flush_page(op[1])
    else:
        db.flush_log()


def make_workload(rng: random.Random, n_steps: int, db: MLR, first_txn: int = 1, n_txns: int = 6) -> list:
    ops: list = []
    status: dict[int, str] = {}
    nxt = first_txn
    while len(ops) < n_steps:
        work: list = []
        if len(status) < 3 and nxt < first_txn + n_txns:
            work.append(("begin", nxt))
        for t in sorted(status):
            if db.busy(t):
                if db.can_act(t):
                    work += [("step", t)] * 3
            elif status[t] == "aborting":
                work += [("step", t)] * 3
            else:
                work += [("add", t, rng.choice(KEYS), rng.randint(1, 9))] * 4
                work += [("commit", t), ("abort", t)] if rng.random() < 0.5 else [("commit", t)]
        if not work:
            break
        if rng.random() < 0.2:
            op = rng.choice([("flush", p) for p in PAGES] + [("flush_log",)])
        else:
            op = rng.choice(work)
        apply(db, op)
        ops.append(op)
        if op[0] == "begin":
            status[op[1]] = "active"
            nxt += 1
        elif op[0] == "commit":
            del status[op[1]]
        elif op[0] == "abort":
            status[op[1]] = "aborting"
        elif op[0] == "step" and status[op[1]] == "aborting" and not db.rolling_back(op[1]):
            del status[op[1]]
    return ops


def oracle(base: dict, ops: list, log: list) -> dict:
    won = {r.txn for r in log if r.kind == "commit"}
    exp = dict(base)
    for op in ops:
        if op[0] == "add" and op[1] in won:
            exp[op[2]] += op[3]
            exp["t"] += op[3]
    return exp


def values(db: MLR) -> dict:
    return {k: db.value(k) for k in sorted(INIT)}


def check_done(db: MLR, ops: list, base: dict) -> None:
    assert values(db) == oracle(base, ops, db.log)
    assert not db.tail and not db.undo_next and not db.plan
    ended = {r.txn for r in db.log if r.kind == "end"}
    assert ended == {r.txn for r in db.log if r.txn}
    twice = Counter(r.undone for r in db.log if r.kind == "comp_commit")
    assert not twice or max(twice.values()) == 1


def run_prefix(ops: list, k: int, disk=None, log=None) -> MLR:
    db = MLR(copy.deepcopy(disk) if disk else fresh_disk(), log)
    for op in ops[:k]:
        apply(db, op)
    return db.crash()


def workload(seed: int, n: int = 70) -> list:
    return make_workload(random.Random(seed), n, MLR(fresh_disk()))


def test_crash_at_every_step() -> None:
    for seed in range(6):
        ops = workload(seed)
        for k in range(len(ops) + 1):
            db = run_prefix(ops, k)
            db.recover()
            check_done(db, ops[:k], INIT)


def test_crashes_inside_recovery() -> None:
    for seed in (11, 12):
        ops = workload(seed, 60)
        rng = random.Random(seed)
        for k in range(0, len(ops) + 1, 2):
            n_steps = sum(1 for _ in run_prefix(ops, k).restart())
            for j in range(n_steps + 1):
                db = run_prefix(ops, k)
                gen = db.restart()
                for _ in range(j):
                    next(gen)
                for p in PAGES:
                    if rng.random() < 0.5:
                        db.flush_page(p)
                if rng.random() < 0.5:
                    db.flush_log()
                db = db.crash()
                db.recover()
                check_done(db, ops[:k], INIT)


def test_two_crashes_inside_recovery() -> None:
    rng = random.Random(21)
    ops = workload(21, 60)
    for k in range(0, len(ops) + 1, 3):
        for _ in range(4):
            db = run_prefix(ops, k)
            for _ in range(2):
                gen = db.restart()
                for _ in range(rng.randint(0, 25)):
                    if next(gen, "done") == "done":
                        break
                for p in PAGES:
                    if rng.random() < 0.6:
                        db.flush_page(p)
                db = db.crash()
            db.recover()
            check_done(db, ops[:k], INIT)


def test_second_epoch_after_recovery() -> None:
    ops1 = workload(31, 50)
    db = run_prefix(ops1, len(ops1))
    db.recover()
    for p in PAGES:
        db.flush_page(p)
    base = values(db)
    disk, log = copy.deepcopy(db.disk), list(db.log)
    ops2 = make_workload(random.Random(32), 50, MLR(copy.deepcopy(disk), log), first_txn=100)
    for k in range(len(ops2) + 1):
        db2 = run_prefix(ops2, k, disk, log)
        db2.recover()
        assert values(db2) == oracle(base, ops2[:k], db2.log)


def example_db() -> MLR:
    db = MLR(fresh_disk())
    db.begin(1)
    db.add(1, "a", 5)
    for _ in range(3):
        db.step(1)
    db.flush_page("P1")  # steal: a = 15 reaches the disk
    db.begin(2)
    db.add(2, "a", 7)
    for _ in range(3):
        db.step(2)
    db.commit(2)
    db.begin(3)
    db.add(3, "c", 4)
    db.step(3)
    db.flush_page("P2")  # the WAL rule forces the log to LSN 11
    return db.crash()


def test_hand_example() -> None:
    db = example_db()
    assert [r.kind for r in db.log] == ["begin", "update", "update", "op_commit", "begin", "update",
                                       "update", "op_commit", "commit", "end", "begin", "update"]
    db.recover()
    assert values(db) == {"a": 17, "b": 20, "c": 30, "d": 40, "t": 107}
    new = [(r.lsn, r.kind, r.txn, r.key, r.before, r.after) for r in db.log[12:]]
    assert new == [
        (13, "clr", 3, "c", 0, 30),
        (14, "end", 3, "", 0, 0),
        (15, "update", 1, "a", 22, 17),
        (16, "update", 1, "t", 112, 107),
        (17, "comp_commit", 1, "", 0, 0),
        (18, "end", 1, "", 0, 0),
    ]
    assert db.log[16].undo_next == 1 and db.log[16].undone == 4


def test_physical_undo_of_completed_operations_is_wrong() -> None:
    db = example_db()
    db.physical_undo = True
    db.recover()
    # T2 committed +7 on a, but the before images of T1 put a back to 10.
    assert values(db)["a"] == 10 and values(db)["t"] == 100


def test_level0_locks_are_released_at_operation_end() -> None:
    db = MLR(fresh_disk())
    db.begin(1)
    db.add(1, "a", 1)
    db.step(1)
    db.begin(2)
    db.add(2, "a", 2)
    assert not db.can_act(2)  # T1 still runs its ADD on a
    db.step(1)
    db.step(1)  # op_commit
    assert db.can_act(2)  # T1 has not committed, but its level 0 locks are gone
