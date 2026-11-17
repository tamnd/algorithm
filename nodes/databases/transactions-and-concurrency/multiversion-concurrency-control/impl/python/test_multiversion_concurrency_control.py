# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiversion-concurrency-control/. The authors are listed in prov/07QKP2.jsonl.

import random
from itertools import permutations

from multiversion_concurrency_control import Mvto

ITEMS = ["x", "y", "z"]


def run(seed: int, n: int, gc_every: int = 0):
    """A random interleaving of n transactions. Returns the scheduler and the
    number of versions after each step."""
    rng = random.Random(seed)
    db = Mvto({x: 0 for x in ITEMS})
    progs, ts, sizes, step = {}, {}, [], 0
    for i in range(n):
        ops = [(rng.choice("rw"), rng.choice(ITEMS)) for _ in range(rng.randrange(1, 5))]
        progs[i] = ops + [("c", None)]
    while progs:
        i = rng.choice(sorted(progs))
        if i not in ts:
            ts[i] = db.begin()
        t = ts[i]
        k, x = progs[i][0]
        if db.status[t] == "aborted":
            del progs[i]
            continue
        if k == "r":
            db.read(t, x)
        elif k == "w":
            db.write(t, x, (t, x))
        else:
            r = db.try_commit(t)
            if r == "wait":
                continue
        progs[i].pop(0)
        if not progs[i] or db.status[t] == "aborted":
            del progs[i]
        step += 1
        if gc_every and step % gc_every == 0:
            db.gc()
        sizes.append(sum(len(vs) for vs in db.versions.values()))
    return db, sizes


def one_copy_serial_orders(db: Mvto) -> list[tuple]:
    """All serial orders of the committed transactions that are view
    equivalent to the history on one copy: every read reads from the same
    writer, and the last writer of each item is the same."""
    com = sorted(t for t, s in db.status.items() if s == "committed")
    final = {x: max((t for t in com if x in db.written[t]), default=0) for x in ITEMS}
    found = []
    for order in permutations(com):
        last = {x: 0 for x in ITEMS}
        ok = True
        for t in order:
            for x, w in db.reads_from[t]:
                want = t if x in db.written[t] and w == t else last[x]
                if w != want:
                    ok = False
            for x in db.written[t]:
                last[x] = t
        if ok and last == final:
            found.append(order)
    return found


def test_mvto_histories_are_one_copy_serializable_in_timestamp_order() -> None:
    aborts = commits = 0
    for seed in range(400):
        db, _ = run(seed, random.Random(seed).randrange(2, 6))
        orders = one_copy_serial_orders(db)
        com = tuple(sorted(t for t, s in db.status.items() if s == "committed"))
        assert com in orders, seed  # the timestamp order is one of them
        aborts += sum(1 for s in db.status.values() if s == "aborted")
        commits += len(com)
    assert aborts > 20 and commits > 500


def test_reads_never_wait_or_abort() -> None:
    db = Mvto({"x": 0})
    t1, t2 = db.begin(), db.begin()
    assert db.write(t2, "x", 2)
    assert db.read(t1, "x") == 0  # t1 is older: it reads the old version
    assert db.read(t2, "x") == 2
    assert db.try_commit(t1) == "committed" and db.try_commit(t2) == "committed"


def test_late_write_aborts() -> None:
    db = Mvto({"x": 0})
    t1, t2 = db.begin(), db.begin()
    assert db.read(t2, "x") == 0  # rts of x_0 becomes 2
    assert not db.write(t1, "x", 1)  # t2 should have read t1's version
    assert db.status[t1] == "aborted"


def test_cascading_abort_and_commit_dependency() -> None:
    db = Mvto({"x": 0})
    t1, t2 = db.begin(), db.begin()
    db.write(t1, "x", 1)
    assert db.read(t2, "x") == 1  # reads an uncommitted version
    assert db.try_commit(t2) == "wait"
    db.abort(t1)
    assert db.status[t2] == "aborted"
    assert [v.wts for v in db.versions["x"]] == [0]


def test_gc_keeps_results_and_bounds_versions() -> None:
    for seed in range(150):
        n = random.Random(seed).randrange(2, 6)
        a, sa = run(seed, n)
        b, sb = run(seed, n, gc_every=2)
        assert a.status == b.status and a.reads_from == b.reads_from
        assert max(sb) <= max(sa)
    db = Mvto({"x": 0})
    for i in range(50):
        t = db.begin()
        db.write(t, "x", i)
        db.try_commit(t)
    assert len(db.versions["x"]) == 51
    db.gc()
    assert len(db.versions["x"]) == 1 and db.versions["x"][0].value == 49
