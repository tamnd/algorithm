# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/key-range-locking/. The authors are listed in prov/VVNHG6.jsonl.

import random

import pytest

import dbsched
import key_range_locking as krl
from key_range_locking import EOF, S, X

KEYS = [2, 5, 7]


def test_next_key_and_the_locks_of_each_operation() -> None:
    idx = krl.KeyRangeIndex(KEYS)
    assert idx.next_key(5) == 7 and idx.next_key(4) == 5 and idx.next_key(7) == EOF
    assert idx.needs(("scan", 3, 6)) == [(5, S, False), (7, S, False)]
    assert idx.needs(("scan", 6, 8)) == [(7, S, False), (EOF, S, False)]
    assert idx.needs(("fetch", 4)) == [(5, S, False)]
    assert idx.needs(("fetch", 5)) == [(5, S, False)]
    assert idx.needs(("insert", 4)) == [(5, X, True), (4, X, False)]
    assert idx.needs(("insert", 5)) == [(5, S, False)]
    assert idx.needs(("delete", 5)) == [(5, X, False), (7, X, False)]
    assert idx.needs(("delete", 4)) == [(5, S, False)]


def test_instant_lock_is_not_kept() -> None:
    lm = krl.LockManager()
    assert lm.try_lock(1, 5, X, instant=True) and lm.mode(1, 5) is None
    assert lm.try_lock(2, 5, S) and not lm.try_lock(1, 5, X, instant=True)
    assert lm.waits_for() == {(1, 2)}


def check_state(idx, touched):
    """The cover invariant: for every slot that an active transaction used,
    it holds a lock on the key that covers the slot now, X if it wrote it."""
    for t, slots in touched.items():
        for v, kind in slots.items():
            cov = v if idx.present(v) else idx.next_key(v)
            m = idx.lm.mode(t, cov)
            assert m is not None and (kind == "r" or m == X), (t, v, cov, m)


def violations(keys, programs, results, out, final):
    """The ways in which a run is not like the serial run in commit order."""
    bad = []
    order = [a[1] for a in out if a[0] == "c"]
    want, want_final = krl.serial_results(keys, {t: programs[t] for t in order}, order)
    if want != results or want_final != final:
        bad.append("results")
    cp = dbsched.committed_projection(out)
    if not dbsched.conflict_equivalent(cp, dbsched.serial_schedule(cp, order)):
        bad.append("conflicts")
    if not dbsched.is_strict(out):
        bad.append("strict")
    if len(order) <= 3 and not dbsched.is_conflict_serializable(out):
        bad.append("serializable")
    return bad


def _arrivals(programs):
    seqs = [[("r", t, "x")] * (len(programs[t]) + 1) for t in sorted(programs)]
    for a in dbsched.interleavings(seqs):
        yield [x[1] for x in a]


def test_the_phantom_is_blocked() -> None:
    programs = {1: [("scan", 3, 6), ("scan", 3, 6)], 2: [("insert", 4)]}
    arrival = [1, 2, 1, 1, 2]
    results, out, final = krl.run(KEYS, programs, arrival, check=check_state)
    assert results == {1: [(5,), (5,)], 2: [True]} and final == (2, 4, 5, 7)
    assert dbsched.format(out) == "r1(k3) r1(k4) r1(k5) r1(k6) r1(k3) r1(k4) r1(k5) r1(k6) c1 w2(k4) c2"
    # Without the lock on the next key, the insert gets in between the two scans.
    results, out, final = krl.run(KEYS, programs, arrival, naive=True)
    assert results[1] == [(5,), (4, 5)]
    assert not dbsched.is_conflict_serializable(out)


def test_deadlock_and_undo() -> None:
    # Both scan, then both insert into the scanned range: each instant X waits for the other.
    programs = {1: [("scan", 3, 6), ("insert", 4)], 2: [("insert", 1), ("scan", 3, 6), ("insert", 6)]}
    arrival = [2, 1, 2, 1, 2, 1, 2]
    results, out, final = krl.run(KEYS, programs, arrival, check=check_state)
    assert ("a", 2, None) in out and results == {1: [(5,), True]}
    assert final == (2, 4, 5, 7)  # the insert of 1 by T2 is undone
    assert violations(KEYS, programs, results, out, final) == []


PROGRAMS = [
    {1: [("scan", 3, 6), ("scan", 3, 6)], 2: [("insert", 4)]},
    {1: [("fetch", 4), ("fetch", 4)], 2: [("insert", 4), ("delete", 5)]},
    {1: [("fetch", 8), ("scan", 6, 8)], 2: [("insert", 8)]},  # the gap below EOF
    {1: [("delete", 5), ("insert", 3)], 2: [("scan", 4, 6), ("fetch", 3)]},
]


@pytest.mark.parametrize("programs", PROGRAMS)
def test_all_interleavings(programs) -> None:
    naive_bad = 0
    for arrival in _arrivals(programs):
        results, out, final = krl.run(KEYS, programs, arrival, check=check_state)
        assert violations(KEYS, programs, results, out, final) == []
        r, o, f = krl.run(KEYS, programs, arrival, naive=True)
        naive_bad += bool(violations(KEYS, programs, r, o, f))
    assert naive_bad > 0  # every one of these pairs has a phantom without next-key locks


def random_programs(rng, n):
    programs = {}
    for t in range(1, n + 1):
        ops = []
        for _ in range(rng.randint(1, 3)):
            kind = rng.choice(["scan", "fetch", "insert", "insert", "delete"])
            if kind == "scan":
                lo = rng.randint(1, 8)
                ops.append((kind, lo, min(8, lo + rng.randint(0, 3))))
            else:
                ops.append((kind, rng.randint(1, 8)))
        programs[t] = ops
    return programs


def test_random_interleavings() -> None:
    rng = random.Random(4)
    aborts, naive_bad = 0, 0
    for n in [3] * 400 + [5] * 200:
        keys = sorted(rng.sample(range(1, 9), rng.randint(2, 5)))
        programs = random_programs(rng, n)
        arrival = [t for t in programs for _ in range(len(programs[t]) + 1)]
        rng.shuffle(arrival)
        results, out, final = krl.run(keys, programs, arrival, check=check_state)
        assert violations(keys, programs, results, out, final) == []
        aborts += bool(dbsched.aborted(out))
        r, o, f = krl.run(keys, programs, arrival, naive=True)
        naive_bad += bool(violations(keys, programs, r, o, f))
    assert aborts > 0 and naive_bad > 0
