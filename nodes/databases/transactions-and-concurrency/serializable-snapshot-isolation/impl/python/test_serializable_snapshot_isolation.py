# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/serializable-snapshot-isolation/. The authors are listed in prov/04RT24.jsonl.

import random
from itertools import permutations

import pytest

from serializable_snapshot_isolation import Aborted, SsiDb

ITEMS = ["x", "y", "z"]


def serializable(db: SsiDb) -> bool:
    """Brute force: is there a serial order of the committed transactions in
    which every read reads from the same writer and every item ends with the
    same final writer (one-copy serializability)?"""
    com = [t for t, s in db.state.items() if s == "committed"]
    reads = {t: [(x, w) for u, x, w in db.reads if u == t and w != t] for t in com}
    final = {x: max(vs, key=lambda v: v[0])[2] for x, vs in db.versions.items()}
    for order in permutations(com):
        last = {x: 0 for x in db.versions}
        ok = True
        for t in order:
            if any(last[x] != w for x, w in reads[t]):
                ok = False
                break
            for x in db.written[t]:
                last[x] = t
        if ok and last == final:
            return True
    return False


def run(seed: int, ssi: bool, n: int = 4) -> SsiDb:
    rng = random.Random(seed)
    db = SsiDb({x: 0 for x in ITEMS}, ssi=ssi)
    todo = {t: [(rng.choice("rw"), rng.choice(ITEMS)) for _ in range(rng.randrange(2, 5))] + [("c", None)]
            for t in range(1, n + 1)}
    began = set()
    while todo:
        t = rng.choice(sorted(todo))
        if t not in began:  # begin is a step of its own, so starts differ
            db.begin(t)
            began.add(t)
            continue
        k, x = todo[t].pop(0)
        try:
            if k == "r":
                db.read(t, x)
            elif k == "w":
                db.write(t, x, (t, x))
            else:
                db.commit(t)
        except Aborted:
            del todo[t]
            continue
        if not todo[t]:
            del todo[t]
    return db


def test_committed_histories_are_serializable() -> None:
    si_bad = false_pos = 0
    for seed in range(3000):
        db = run(seed, ssi=True)
        assert serializable(db), seed
        assert all(not h for h in db.siread.values())  # all locks released at the end
        plain = run(seed, ssi=False)
        si_bad += not serializable(plain)
        unsafe = any(w != "first committer wins" for w in db.why.values())
        false_pos += unsafe and serializable(plain) and all(s == "committed" for s in plain.state.values())
    assert si_bad > 0  # plain SI does commit non-serializable histories
    assert false_pos > 0  # and SSI sometimes aborts where SI was serializable


def doctors() -> SsiDb:
    db = SsiDb({"a": 1, "b": 1})  # both doctors on call
    db.begin(1)
    db.begin(2)
    for t in (1, 2):
        assert db.read(t, "a") + db.read(t, "b") == 2  # each sees two on call
    return db


def test_write_skew_is_aborted() -> None:
    db = doctors()
    db.write(1, "a", 0)  # T2 holds an SIREAD lock on a: T2 -rw-> T1
    db.commit(1)  # T1 has only an in edge: commits
    with pytest.raises(Aborted):
        db.write(2, "b", 0)  # T1 committed with an in edge read b: T1 would be a pivot
    assert db.why[2] == "unsafe write"
    assert (db.value("a"), db.value("b")) == (0, 1)


def test_write_skew_both_writes_first() -> None:
    db = doctors()
    db.write(1, "a", 0)
    db.write(2, "b", 0)  # now both have an in and an out edge
    with pytest.raises(Aborted):
        db.commit(1)
    with pytest.raises(Aborted):
        db.commit(2)  # a false positive: T1 is gone, T2 alone was safe
    assert db.why == {1: "pivot", 2: "pivot"}
    assert (db.value("a"), db.value("b")) == (1, 1)


def test_plain_si_allows_write_skew() -> None:
    db = SsiDb({"a": 1, "b": 1}, ssi=False)
    db.begin(1)
    db.begin(2)
    for t in (1, 2):
        db.read(t, "a")
        db.read(t, "b")
    db.write(1, "a", 0)
    db.write(2, "b", 0)
    db.commit(1)
    db.commit(2)
    assert (db.value("a"), db.value("b")) == (0, 0)
    assert not serializable(db)


def chain(ssi: bool) -> SsiDb:
    """r1(x) r2(y) w2(x) w3(y) w1(z) c3 c2 c1: T1 -rw-> T2 -rw-> T3, no cycle."""
    db = SsiDb({x: 0 for x in ITEMS}, ssi=ssi)
    for t in (1, 2, 3):
        db.begin(t)
    db.read(1, "x")
    db.read(2, "y")
    db.write(2, "x", 2)
    db.write(3, "y", 3)
    db.write(1, "z", 1)
    db.commit(3)
    try:
        db.commit(2)
    except Aborted:
        pass
    db.commit(1)
    return db


def test_false_positive_abort() -> None:
    plain = chain(ssi=False)
    assert all(s == "committed" for s in plain.state.values())
    assert serializable(plain)  # equivalent to T1 T2 T3
    db = chain(ssi=True)
    assert db.state == {1: "committed", 2: "aborted", 3: "committed"}
    assert db.why == {2: "pivot"}


def test_committed_pivot_on_read() -> None:
    # T2 reads y, T3 writes y and commits: T2 -rw-> T3. T2 writes x and
    # commits with an out edge. T1 then reads x and finds T2's newer version:
    # T1 -rw-> T2 would make the committed T2 a pivot, so T1 aborts.
    db = SsiDb({x: 0 for x in ITEMS})
    for t in (1, 2, 3):
        db.begin(t)
    db.read(2, "y")
    db.write(3, "y", 3)
    db.commit(3)
    db.write(2, "x", 2)
    db.commit(2)
    with pytest.raises(Aborted):
        db.read(1, "x")
    assert db.why == {1: "unsafe read"}
