# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aries-recovery/. The authors are listed in prov/YSPCY5.jsonl.

import random
from collections import Counter

from aries_recovery import Aries, state

PAGES = {"P": ["a", "b"], "Q": ["c", "d"], "R": ["e"]}


KEYS = [(p, k) for p, keys in PAGES.items() for k in keys]


def fresh_disk():
    """P: a = 10, b = 20; Q: c = 30, d = 40; R: e = 50; every pageLSN is 0."""
    disk = {p: ({}, 0) for p in PAGES}
    for i, (p, k) in enumerate(KEYS):
        disk[p][0][k] = 10 * (i + 1)
    return disk


def make_workload(rng: random.Random, steps: int, first_txn: int = 1, disk=None, log=None, master=0):
    """Random strict workload, generated against a live system so that each op
    is valid. Returns the op list and the write journal used by the oracle."""
    db = Aries(disk or fresh_disk(), log, master)
    ops: list[tuple] = []
    locks: dict[int, set] = {}
    aborting: set[int] = set()
    nxt, val = first_txn, 1000 * first_txn
    saves: dict[int, int] = {}
    ckpt = 0
    for _ in range(steps):
        c = rng.random()
        running = sorted(t for t in locks if t not in aborting)
        if (c < 0.12 or not locks) and len(locks) < 3:
            locks[nxt] = set()
            nxt += 1
            continue
        if c < 0.45 and running:
            t = rng.choice(running)
            taken = set().union(*(s for u, s in locks.items() if u != t))
            free = [pk for pk in KEYS if pk not in taken]
            if free:
                p, k = rng.choice(free)
                val += 1
                locks[t].add((p, k))
                op = ("update", t, p, k, val)
            else:
                continue
        elif c < 0.52 and running:
            op = ("commit", rng.choice(running))
        elif c < 0.57 and running:
            op = ("begin_abort", rng.choice(running))
        elif c < 0.67 and aborting:
            op = ("undo_step", rng.choice(sorted(aborting)))
        elif c < 0.71 and running:
            t = rng.choice(running)
            if t in saves:
                op = ("rollback_to", t, saves.pop(t))
            else:
                saves[t] = db.savepoint(t)
                continue
        elif c < 0.84 and db.buf:
            op = ("flush_page", rng.choice(sorted(db.buf)))
        elif c < 0.9:
            op = ("flush_log",)
        elif c < 0.95 and not ckpt:
            op = ("begin_ckpt",)
        elif ckpt:
            op = ("end_ckpt",)
        else:
            continue
        ckpt = apply(db, op, ckpt)
        ops.append(op)
        if op[0] == "commit":
            del locks[op[1]]
            saves.pop(op[1], None)
        elif op[0] == "begin_abort":
            aborting.add(op[1])
        elif op[0] == "undo_step" and op[1] not in db.att:
            aborting.discard(op[1])
            del locks[op[1]]
    return ops


def apply(db: Aries, op: tuple, ckpt: int = 0) -> int:
    kind = op[0]
    if kind == "update":
        db.update(*op[1:])
    elif kind == "commit":
        db.commit(op[1])
    elif kind == "begin_abort":
        db.begin_abort(op[1])
    elif kind == "undo_step":
        db.undo_step(op[1])
    elif kind == "rollback_to":
        db.rollback_to(op[1], op[2])
    elif kind == "flush_page":
        db.flush_page(op[1])
    elif kind == "flush_log":
        db.flush_log(db.next_lsn)
    elif kind == "begin_ckpt":
        return db.begin_checkpoint()
    elif kind == "end_ckpt":
        db.end_checkpoint(ckpt)
        return 0
    return ckpt


def oracle(start: dict, log, ops: list[tuple]) -> dict:
    """The last surviving write of each key by a transaction whose commit
    record is in the stable log. Undo by rollback is read from the op list."""
    committed = {r.txn for r in log if r.kind == "commit"}
    writes: list[list] = []  # [txn, key, value, alive]
    for op in ops:
        if op[0] == "update":
            writes.append([op[1], (op[2], op[3]), op[4], True])
    # rolled back writes: replay rollbacks from a fresh run of the ops
    db = Aries(fresh_disk())
    alive_lsn = {}
    ck = 0
    i = 0
    for op in ops:
        if op[0] == "update":
            alive_lsn[db.next_lsn] = i
            i += 1
        ck = apply(db, op, ck)
    for r in list(db.log) + db.tail:
        if r.kind == "clr" and r.undone in alive_lsn:
            writes[alive_lsn[r.undone]][3] = False
    st = dict(start)
    for t, key, v, alive in writes:
        if alive and t in committed:
            st[key] = v
    return st


def replay(ops, k, disk=None, log=None, master=0):
    db = Aries(disk or fresh_disk(), log, master)
    ck = 0
    for op in ops[:k]:
        ck = apply(db, op, ck)
    return db


def at_most_one_clr_per_update(log) -> bool:
    c = Counter(r.undone for r in log if r.kind == "clr")
    return all(n == 1 for n in c.values())


def test_crash_at_every_step() -> None:
    start = state(fresh_disk())
    for seed in range(40):
        ops = make_workload(random.Random(seed), 90)
        for k in range(len(ops) + 1):
            db = replay(ops, k)
            disk, log, master = db.crash()
            want = oracle(start, log, ops[:k])
            assert db.acked <= {r.txn for r in log if r.kind == "commit"}
            r = Aries(disk, log, master)
            assert r.recover()
            assert r.current() == want, (seed, k)
            d2, log2, m2 = r.crash()  # crash right after recovery, before any page write
            r3 = Aries(d2, log2, m2)
            assert r3.recover() and r3.current() == want
            assert at_most_one_clr_per_update(log2)


def test_crashes_inside_recovery() -> None:
    start = state(fresh_disk())
    rng = random.Random(99)
    for seed in range(25):
        ops = make_workload(random.Random(seed), 80)
        for k in range(0, len(ops) + 1, 4):
            disk, log, master = replay(ops, k).crash()
            want = oracle(start, log, ops[:k])
            updates = sum(1 for r in log if r.kind == "update")
            for _ in range(4):  # several crashes in a row, each at a random step
                r = Aries(disk, log, master)
                if r.recover(stop_after=rng.randrange(1, 25), flushes=rng):
                    break
                disk, log, master = r.crash()
            r = Aries(disk, log, master)
            assert r.recover(flushes=rng)
            assert r.current() == want
            d2, log2, m2 = r.crash()
            assert at_most_one_clr_per_update(log2)
            clrs = sum(1 for x in log2 if x.kind == "clr")
            assert clrs <= updates  # the log grows by at most one CLR per update


def test_second_epoch_after_recovery() -> None:
    for seed in range(15):
        ops = make_workload(random.Random(seed), 60)
        disk, log, master = replay(ops, len(ops)).crash()
        r = Aries(disk, log, master)
        r.recover()
        start = r.current()
        for p in sorted(r.buf):
            r.flush_page(p)
        disk, log, master = r.crash()
        assert state(disk) == start
        ops2 = make_workload(random.Random(1000 + seed), 60, first_txn=500, disk=disk, log=log, master=master)
        for k in range(len(ops2) + 1):
            db = replay(ops2, k, disk, log, master)
            d, lg, m = db.crash()
            committed = {x.txn for x in lg if x.kind == "commit" and x.txn >= 500}
            writes = {}
            clr_undone = {x.undone for x in lg + db.tail if x.kind == "clr"}
            for x in lg + db.tail:
                if x.kind == "update" and x.txn in committed and x.lsn not in clr_undone:
                    writes[(x.page, x.key)] = x.after
            want = dict(start)
            want.update(writes)
            r2 = Aries(d, lg, m)
            r2.recover()
            assert r2.current() == want


def test_hand_example() -> None:
    # T1 changes a and c, T2 changes b on the same page as a, a fuzzy checkpoint
    # is taken, T2 commits, page P is stolen, then a crash.
    db = Aries(fresh_disk())
    db.update(1, "P", "a", 11)  # LSN 1
    db.update(2, "P", "b", 21)  # LSN 2
    b = db.begin_checkpoint()  # LSN 3
    db.end_checkpoint(b)  # LSN 4
    db.update(1, "Q", "c", 31)  # LSN 5
    db.commit(2)  # LSN 6 commit, LSN 7 end
    db.flush_page("P")
    disk, log, master = db.crash()
    assert master == 3
    assert [r.lsn for r in log] == [1, 2, 3, 4, 5, 6]
    assert log[3].att == ((1, "U", 1, 1), (2, "U", 2, 2)) and log[3].dpt == (("P", 1),)
    assert disk["P"] == ({"a": 11, "b": 21}, 2) and disk["Q"] == ({"c": 30, "d": 40}, 0)
    r = Aries(disk, log, master)
    assert r.recover()
    d2, log2, _ = r.crash()
    assert r.current() == {("P", "a"): 10, ("P", "b"): 21, ("Q", "c"): 30, ("Q", "d"): 40, ("R", "e"): 50}
    tail = [(x.lsn, x.kind, x.txn, x.undo_next) for x in log2[6:9]]
    assert tail == [(7, "end", 2, 0), (8, "clr", 1, 1), (9, "clr", 1, 0)]
    assert log2[9].kind == "end" and log2[9].txn == 1


def test_partial_rollback_skips_compensated_updates() -> None:
    db = Aries(fresh_disk())
    db.update(1, "P", "a", 1)
    s = db.savepoint(1)
    db.update(1, "P", "a", 2)
    db.update(1, "Q", "c", 3)
    db.rollback_to(1, s)
    db.update(1, "R", "e", 4)
    assert db.read("P", "a") == 1 and db.read("Q", "c") == 30
    disk, log, master = db.crash()
    db2 = Aries(disk, log, master)
    db2.recover()
    assert db2.current() == state(fresh_disk())
    # The full log: every update undone by exactly one CLR.
    db.flush_log(db.next_lsn)
    db.begin_abort(1)
    while not db.undo_step(1):
        pass
    db.flush_log(db.next_lsn)
    assert at_most_one_clr_per_update(db.log)
    assert sum(1 for r in db.log if r.kind == "clr") == 4
