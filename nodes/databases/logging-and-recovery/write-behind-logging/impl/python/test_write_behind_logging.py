# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-behind-logging/. The authors are listed in prov/80XPYE.jsonl.

"""Write-behind logging checked by crash injection.

A random workload with evictions, aborts and group commits is cut by a crash
after every prefix, recovered, continued and cut again. The visible state must
be the effect of exactly the reported transactions.
"""

import random

from write_behind_logging import INIT, LogRec, WblDb, in_gap

KEYS = sorted(INIT)


def run(db: WblDb, rng: random.Random, steps: int, committed: dict) -> None:
    """Random actions; committed gets the writes of each reported group."""
    groups: dict[int, dict] = {}
    open_txn = None
    writes: dict = {}
    for _ in range(steps):
        r = rng.random()
        if open_txn is None and db.next_ts >= db.log[-1].cd:
            for ts in db.group_commit():  # the group is full
                committed.update(groups.pop(ts))
        elif open_txn is None and r < 0.3:
            open_txn, writes = db.begin(), {}
        elif open_txn is not None and r < 0.6:
            k, v = rng.choice(KEYS), rng.randint(100, 999)
            db.write(open_txn, k, v)
            writes[k] = v
        elif open_txn is not None and r < 0.7:
            db.commit(open_txn)
            groups[open_txn] = writes
            open_txn = None
        elif open_txn is not None and r < 0.75:
            db.abort(open_txn)
            open_txn = None
        elif r < 0.9:
            db.evict(rng.randrange(1000))
        elif open_txn is None:
            for ts in db.group_commit():
                committed.update(groups.pop(ts))


def test_crash_at_every_prefix_twice() -> None:
    for seed in range(5):
        for k in range(0, 61, 3):
            rng = random.Random(seed)
            db, committed = WblDb(group=8), dict(INIT)
            run(db, rng, k, committed)
            db = db.crash()
            db.recover()
            assert db.records_read == 1
            assert db.state() == committed
            run(db, random.Random(seed + 100), 40, committed)  # new work after the restart
            db = db.crash()
            db.recover()
            assert db.state() == committed


def test_garbage_collection_removes_the_gaps() -> None:
    rng = random.Random(4)
    db, committed = WblDb(group=8), dict(INIT)
    for _ in range(5):
        run(db, rng, 50, committed)
        db = db.crash()
        db.recover()
    while db.gc_step():
        pass
    assert db.state() == committed
    assert not any(in_gap(v.ts, db.log[-1].gaps) for v in db.nvm)
    ts = db.begin()
    db.commit(ts)
    db.group_commit()
    assert db.log[-1].gaps == ()  # every gap is empty, so the next record drops them


def test_hand_example() -> None:
    db = WblDb(group=100)
    t1 = db.begin()  # timestamp 1
    db.write(t1, "a", 11)
    db.commit(t1)
    assert db.group_commit() == [1]
    assert db.log[-1] == LogRec(1, 101, ())
    t2 = db.begin()  # timestamp 2
    db.write(t2, "b", 22)
    db.commit(t2)
    db.evict(0)  # b = 22 reaches NVM before the group commits
    db = db.crash()
    assert [(v.key, v.ts) for v in db.nvm] == [("a", 1), ("b", 2)]
    db.recover()  # no redo and no undo
    assert db.log[-1] == LogRec(101, 201, ((1, 101),))
    assert db.state() == dict(INIT, a=11)  # version 2 lies in the gap (1, 101)
    t3 = db.begin()
    assert t3 == 102
    db.write(t3, "b", 23)
    db.commit(t3)
    db.group_commit()
    assert db.log[-1] == LogRec(102, 202, ((1, 101),))
    assert db.gc_step() and not db.gc_step()
    assert db.state() == dict(INIT, a=11, b=23)
