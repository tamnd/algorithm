# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/snapshot-isolation/. The authors are listed in prov/ZZY45M.jsonl.

import random
from itertools import permutations

import pytest

from snapshot_isolation import Aborted, SnapshotDb


def test_doctors_on_call_write_skew() -> None:
    # Constraint: at least one doctor is on call. Each transaction checks that
    # two are on call, then takes itself off call.
    db = SnapshotDb({"alice": True, "bob": True})
    on1 = db.read(1, "alice") + db.read(1, "bob")  # r1(alice) r1(bob)
    on2 = db.read(2, "alice") + db.read(2, "bob")  # r2(alice) r2(bob)
    assert on1 == on2 == 2
    db.write(1, "alice", False)  # w1(alice)
    db.write(2, "bob", False)  # w2(bob)
    db.commit(1)  # c1
    db.commit(2)  # c2: the write sets are disjoint, so both commit
    assert db.snapshot() == {"alice": False, "bob": False}  # no one is on call
    # Neither serial order gives this: the second transaction would see one doctor.
    for order in permutations([("alice", 1), ("bob", 2)]):
        state = {"alice": True, "bob": True}
        for me, _ in order:
            if sum(state.values()) >= 2:
                state[me] = False
        assert sum(state.values()) == 1


def test_first_committer_wins_prevents_lost_update() -> None:
    db = SnapshotDb({"x": 100})
    a = db.read(1, "x")
    b = db.read(2, "x")
    db.write(1, "x", a + 20)
    db.write(2, "x", b + 30)
    db.commit(1)
    with pytest.raises(Aborted):
        db.commit(2)
    assert db.snapshot()["x"] == 120


def test_snapshot_read_prevents_read_skew() -> None:
    db = SnapshotDb({"x": 50, "y": 50})
    assert db.read(1, "x") == 50
    db.write(2, "x", 10)
    db.write(2, "y", 90)
    db.commit(2)
    assert db.read(1, "y") == 50  # the snapshot of T1, total 100
    db.commit(1)  # read-only transactions always commit


def run_random(rng: random.Random, n: int):
    items = ["x", "y", "z"]
    db = SnapshotDb({x: 0 for x in items})
    progs = {}
    for t in range(1, n + 1):
        ops = [("r", rng.choice(items)) for _ in range(rng.randrange(1, 3))]
        ops += [("w", x) for x in rng.sample(items, rng.randrange(0, 3))]
        progs[t] = ops + [("c", None)]
    seen: dict[int, dict] = {t: {} for t in progs}
    while progs:
        t = rng.choice(sorted(progs))
        k, x = progs[t].pop(0)
        try:
            if k == "r":
                seen[t][x] = db.read(t, x)
            elif k == "w":
                db.write(t, x, (t, x))
            else:
                db.commit(t)
        except Aborted:
            progs[t] = []
        if not progs[t]:
            del progs[t]
    return db, seen


def serializable(db: SnapshotDb, seen: dict) -> bool:
    """Is there a serial order of the committed transactions in which every
    read returns the same value and the final state is the same?"""
    ts = sorted(db.committed)
    final = db.snapshot()
    for order in permutations(ts):
        state = {x: 0 for x in final}
        ok = True
        for t in order:
            for x, v in seen[t].items():
                if x not in db.writes[t] and state[x] != v:
                    ok = False
            for x, v in db.writes[t].items():
                state[x] = v
        if ok and state == final:
            return True
    return False


def test_random_histories_satisfy_the_definition() -> None:
    rng = random.Random(11)
    anomalies = 0
    for _ in range(1500):
        db, seen = run_random(rng, rng.randrange(2, 5))
        c = db.committed
        for t, reads in seen.items():
            for x, v in reads.items():
                if x in db.writes[t] and db.writes[t][x] == v:
                    continue  # read its own write
                assert v == db.snapshot(db.start[t])[x]  # the snapshot at start
        for t1 in c:
            for t2 in c:
                concurrent = t1 != t2 and db.start[t1] < c[t2] and db.start[t2] < c[t1]
                if concurrent:
                    assert not set(db.writes[t1]) & set(db.writes[t2])
        if not serializable(db, seen):
            anomalies += 1
    assert anomalies > 0  # snapshot isolation is not serializable
