# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/checkpointing/. The authors are listed in prov/3HY3MZ.jsonl.

import random

from checkpointing import Db

ITEMS = ["a", "b", "c", "d", "e"]


def fresh() -> dict:
    return {x: (10 * (i + 1), 0) for i, x in enumerate(ITEMS)}


def workload(rng: random.Random, steps: int, kind: str) -> list[tuple]:
    """A strict random workload with checkpoints of one kind, built against a
    live system so that every op is valid."""
    db = Db(fresh())
    ops, locks, nxt, val, begun, quiesce = [], {}, 1, 100, 0, False
    for _ in range(steps):
        c = rng.random()
        if kind == "consistent" and quiesce and not locks:
            op, quiesce = ("consistent",), False
        elif c < 0.12 and len(locks) < 3 and not quiesce:
            locks[nxt] = set()
            nxt += 1
            continue
        elif c < 0.5 and locks:
            t = rng.choice(sorted(locks))
            free = [x for x in ITEMS if all(x not in s for u, s in locks.items() if u != t)]
            if not free:
                continue
            x = rng.choice(free)
            locks[t].add(x)
            val += 1
            op = ("update", t, x, val)
        elif c < 0.6 and locks:
            op = ("commit", rng.choice(sorted(locks)))
        elif c < 0.65 and locks:
            op = ("abort", rng.choice(sorted(locks)))
        elif c < 0.8 and db.buf:
            op = ("flush_page", rng.choice(sorted(db.buf)))
        elif c < 0.85:
            op = ("flush_log",)
        elif kind == "consistent":
            quiesce = True
            continue
        elif kind == "sharp":
            op = ("sharp",)
        elif not begun:
            op = ("fuzzy_begin",)
        else:
            op = ("fuzzy_end",)
        begun = apply(db, op, begun)
        ops.append(op)
        if op[0] in ("commit", "abort"):
            del locks[op[1]]
    return ops


def apply(db: Db, op: tuple, begun: int) -> int:
    k = op[0]
    if k == "update":
        db.update(*op[1:])
    elif k == "commit":
        db.commit(op[1])
    elif k == "abort":
        db.abort(op[1])
    elif k == "flush_page":
        db.flush_page(op[1])
    elif k == "flush_log":
        db.flush_log(db.next_lsn)
    elif k == "consistent":
        db.consistent_checkpoint()
    elif k == "sharp":
        db.sharp_checkpoint()
    elif k == "fuzzy_begin":
        return db.fuzzy_begin()
    elif k == "fuzzy_end":
        db.fuzzy_end(begun)
        return 0
    return begun


def run(ops: list[tuple]) -> Db:
    db, begun = Db(fresh()), 0
    for op in ops:
        begun = apply(db, op, begun)
    return db


def oracle(log) -> dict:
    """With strict locking, an item holds the last write of a transaction whose
    commit or abort record is stable (an abort logs restoring writes)."""
    done = {r.txn for r in log if r.kind in ("commit", "abort")}
    st = {x: v for x, (v, _) in fresh().items()}
    for r in log:
        if r.kind == "update" and r.txn in done:
            st[r.item] = r.after
    return st


def test_restart_from_checkpoint_equals_full_log() -> None:
    for kind in ("consistent", "sharp", "fuzzy"):
        saved = full = 0
        for seed in range(40):
            ops = workload(random.Random(seed), 120, kind)
            for k in range(len(ops) + 1):
                db = run(ops[:k])
                disk, log, master = db.crash()
                assert db.acked <= {r.txn for r in log if r.kind == "commit"}
                a = Db(disk, log, master)
                a.recover()
                b = Db(disk, log, 0)
                b.recover()
                assert a.current() == b.current() == oracle(log), (kind, seed, k)
                saved += a.scanned
                full += b.scanned
        assert saved < full, kind


def test_checkpoints_happen() -> None:
    for kind, rec in (("consistent", "ckpt"), ("sharp", "ckpt"), ("fuzzy", "end_ckpt")):
        db = run(workload(random.Random(7), 200, kind))
        db.flush_log(db.next_lsn)
        assert sum(1 for r in db.log if r.kind == rec) >= 3
        assert db.master > 0


def test_fuzzy_checkpoint_does_not_write_pages() -> None:
    db = Db(fresh())
    db.update(1, "a", 11)
    disk_before = dict(db.disk)
    b = db.fuzzy_begin()
    db.update(2, "b", 21)
    db.fuzzy_end(b)
    assert db.disk == disk_before and db.master == b
    # LSN 1 update a, LSN 2 begin_checkpoint, LSN 3 update b, LSN 4 end_checkpoint
    assert db.log[-1].dpt == (("a", 1), ("b", 3)) and db.log[-1].att == ((1, 1), (2, 3))


def test_redo_from_checkpoint_is_wrong() -> None:
    # T1 writes a and commits; a stays dirty; a fuzzy checkpoint; crash.
    # Redo must start at recLSN 1 < the checkpoint, not at the checkpoint.
    db = Db(fresh())
    db.update(1, "a", 11)  # LSN 1
    db.commit(1)  # LSN 2
    b = db.fuzzy_begin()  # LSN 3
    db.fuzzy_end(b)  # LSN 4
    disk, log, master = db.crash()
    good = Db(disk, log, master)
    good.recover()
    bad = Db(disk, log, master)
    bad.recover(redo_from_checkpoint=True)
    assert good.current()["a"] == 11 and bad.current()["a"] == 10


def test_consistent_checkpoint_bounds_the_scan() -> None:
    db = Db(fresh())
    for t in range(1, 30):
        db.update(t, ITEMS[t % 5], t)
        db.commit(t)
    db.consistent_checkpoint()
    db.update(99, "a", 5)
    db.commit(99)
    disk, log, master = db.crash()
    r = Db(disk, log, master)
    r.recover()
    assert r.scanned == 3 and r.current()["a"] == 5
