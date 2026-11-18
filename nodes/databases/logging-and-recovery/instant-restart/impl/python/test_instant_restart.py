# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instant-restart/. The authors are listed in prov/81XW5M.jsonl.

"""Crash injection for the toy instant restart.

A random workload runs on the database and is cut by a crash after every
prefix. After the restart, new transactions run at once, mixed with
background steps, and every value they read must be the committed value.
"""

import random

from instant_restart import INIT, PAGE_OF, Db, fresh_disk

KEYS = sorted(PAGE_OF)
PAGES = sorted(set(PAGE_OF.values()))


def workload(db: Db, rng: random.Random, steps: int, first_txn: int = 1) -> dict:
    """Run steps random actions. Return the committed state."""
    committed = dict(INIT)
    active: dict[int, dict] = {}  # txn -> its writes
    rolling: list[int] = []
    nxt = first_txn
    for _ in range(steps):
        r = rng.random()
        if r < 0.15 and len(active) < 3:
            db.begin(nxt)
            active[nxt] = {}
            nxt += 1
        elif r < 0.5 and active:
            t = rng.choice(sorted(active))
            k = rng.choice(KEYS)
            v = rng.randint(100, 999)
            if db.write(t, k, v):
                active[t][k] = v
        elif r < 0.6 and active:
            t = rng.choice(sorted(active))
            db.commit(t)
            committed.update(active.pop(t))
        elif r < 0.68 and active:
            t = rng.choice(sorted(active))
            db.abort(t)
            del active[t]
            rolling.append(t)
        elif r < 0.8 and rolling:
            t = rolling[0]
            db.undo_step(t)
            if t not in db.undo_next:
                rolling.pop(0)
        else:
            db.flush_page(rng.choice(PAGES))
    return committed


def instant_phase(db: Db, rng: random.Random, committed: dict, txns: int, first_txn: int,
                  crash_after: int | None = None) -> Db:
    """Run new transactions one after another, with background steps between
    their actions. Check each read. Crash after crash_after actions if given."""
    actions = 0
    for t in range(first_txn, first_txn + txns):
        db.begin(t)
        writes = {}
        for k in rng.sample(KEYS, 2):
            assert db.read(t, k) == committed[k]
            v = rng.randint(1000, 9999)
            assert db.write(t, k, v)
            writes[k] = v
            if rng.random() < 0.5:
                db.background_step()
            if rng.random() < 0.3:
                db.flush_page(rng.choice(PAGES))
            actions += 1
            if crash_after is not None and actions == crash_after:
                return db.crash()
        db.commit(t)
        committed.update(writes)
    return db


def drain_and_check(db: Db, committed: dict) -> None:
    while db.background_step():
        pass
    assert not db.need_redo and not db.losers and not db.undo_next
    assert {k: db.value(k) for k in KEYS} == committed
    assert not db.locks


def test_crash_at_every_prefix() -> None:
    for seed in range(4):
        steps = 60
        for k in range(steps + 1):
            db = Db(fresh_disk())
            committed = workload(db, random.Random(seed), k)
            db = db.crash()
            db.restart()
            rng = random.Random(1000 + 7 * seed + k)
            db = instant_phase(db, rng, committed, txns=4, first_txn=500)
            drain_and_check(db, committed)


def test_crash_during_the_instant_phase() -> None:
    for seed in range(4):
        db = Db(fresh_disk())
        committed = workload(db, random.Random(seed), 50)
        db = db.crash()
        db.restart()
        for cut in range(1, 7):
            probe = Db(dict(db.disk), list(db.log))
            probe.restart()
            rng = random.Random(seed * 31 + cut)
            state = dict(committed)
            crashed = instant_phase(probe, rng, state, txns=4, first_txn=500, crash_after=cut)
            # the new transaction that was cut did not commit; the earlier ones did
            again = Db(dict(crashed.disk), list(crashed.log))
            crashed.restart()
            again.restart()
            drain_and_check(crashed, state)
            # a second restart from the same stable state gives the same values
            drain_and_check(again, state)


def test_crash_during_background_recovery() -> None:
    for seed in range(4):
        db = Db(fresh_disk())
        committed = workload(db, random.Random(seed), 60)
        db = db.crash()
        db.restart()
        rng = random.Random(seed)
        for _ in range(20):
            if not db.background_step():
                break
            if rng.random() < 0.5:
                db.flush_page(rng.choice(PAGES))
            if rng.random() < 0.3:
                db.flush_log()
                db = db.crash()
                db.restart()
        drain_and_check(db, committed)


def test_hand_example() -> None:
    db = Db(fresh_disk())
    db.begin(1)
    db.write(1, "a", 11)
    db.begin(2)
    db.write(2, "c", 31)
    db.write(2, "e", 51)
    db.commit(1)  # forces records 1 to 6
    db.flush_page("P2")  # steal: c = 31 with pageLSN 4 is on disk
    db = db.crash()
    assert len(db.log) == 6
    db.restart()
    assert db.losers == {2} and db.need_redo == {"P1", "P2", "P3"}
    assert db.chain == {"P1": [2], "P2": [4], "P3": [5]}
    assert db.locks == {"c": 2, "e": 2}
    # T3 touches only P1, and only P1 is redone
    db.begin(3)
    assert db.read(3, "a") == 11
    db.write(3, "b", 21)
    db.commit(3)
    assert db.redone == ["P1"] and db.losers == {2}
    # T4 wants c, which the loser T2 holds: T2 is rolled back first
    db.begin(4)
    assert db.write(4, "c", 32)
    assert db.redone == ["P1", "P3", "P2"]
    kinds = [(r.kind, r.txn, r.key, r.after, r.undo_next) for r in map(db.rec, range(7, 17))]
    assert kinds == [("end", 1, "", 0, 0), ("begin", 3, "", 0, 0), ("update", 3, "b", 21, 0),
                     ("commit", 3, "", 0, 0), ("end", 3, "", 0, 0), ("begin", 4, "", 0, 0),
                     ("clr", 2, "e", 50, 4), ("clr", 2, "c", 30, 3), ("end", 2, "", 0, 0),
                     ("update", 4, "c", 32, 0)]
    db.commit(4)
    assert not db.background_step()
    assert {k: db.value(k) for k in KEYS} == {"a": 11, "b": 21, "c": 32, "d": 40, "e": 50, "f": 60}


def test_first_transaction_redoes_only_its_pages() -> None:
    for seed in range(5):
        db = Db(fresh_disk())
        committed = workload(db, random.Random(seed), 80)
        db = db.crash()
        db.restart()
        pending = set(db.need_redo)
        loser_keys = set(db.locks)
        free = [k for k in KEYS if k not in loser_keys]
        if not free:
            continue
        k = free[0]
        db.begin(900)
        assert db.read(900, k) == committed[k]
        assert set(db.redone) <= {PAGE_OF[k]} and set(db.redone) <= pending
        assert db.need_redo == pending - set(db.redone)
