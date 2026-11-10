# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/version-vectors/. The authors are listed in prov/MTVENE.jsonl.

import random

from version_vectors import AFTER, BEFORE, CONCURRENT, EQUAL, Replica, VersionVector, random_ops, sync


def truth(h1: frozenset, h2: frozenset) -> str:
    """Ground truth: compare the sets of updates that two copies contain."""
    if h1 == h2:
        return EQUAL
    if h1 <= h2:
        return BEFORE
    if h2 <= h1:
        return AFTER
    return CONCURRENT


def run(n: int, ops: list[tuple]) -> int:
    reps = [Replica(n, i) for i in range(n)]
    seq = [0] * n
    conflicts = 0
    for op in ops:
        if op[0] == "write":
            i = op[1]
            seq[i] += 1
            reps[i].write((i, seq[i]))
        else:
            _, i, j = op
            want = truth(reps[i].data, reps[j].data)
            got = sync(reps[i], reps[j])
            assert got == want
            conflicts += got == CONCURRENT
        # Invariant: entry k counts the updates of replica k in the copy.
        for r in reps:
            for k in range(n):
                assert r.vv.v[k] == sum(1 for u in r.data if u[0] == k)
        for a in reps:
            for b in reps:
                assert a.vv.compare(b.vv) == truth(a.data, b.data)
    return conflicts


def test_example() -> None:
    a, b, c = Replica(3, 0), Replica(3, 1), Replica(3, 2)
    a.write("A1")
    assert sync(a, b) == AFTER and b.vv.v == [1, 0, 0]
    b.write("B1")
    a.write("A2")
    assert a.vv.v == [2, 0, 0] and b.vv.v == [1, 1, 0]
    assert a.vv.compare(c.vv) == AFTER
    assert sync(a, b) == CONCURRENT
    assert a.vv.v == b.vv.v == [2, 1, 0]
    assert sync(c, a) == BEFORE and c.vv.v == [2, 1, 0]


def test_compare_basic() -> None:
    v, w = VersionVector(2), VersionVector(2)
    assert v.compare(w) == EQUAL
    v.update(0)
    w.update(1)
    assert v.compare(w) == CONCURRENT
    v.merge(w)
    assert v.v == [1, 1] and w.compare(v) == BEFORE


def test_random_against_ground_truth() -> None:
    rng = random.Random(1983)
    total = 0
    for _ in range(500):
        n = rng.randint(1, 5)
        total += run(n, random_ops(n, rng.randint(0, 30), rng))
    assert total > 0  # conflicts do happen in the random runs


def test_partition_then_heal() -> None:
    # Two groups update in isolation, then one sync per pair heals the system.
    n = 4
    ops = [("write", 0), ("sync", 0, 1), ("write", 2), ("sync", 2, 3), ("write", 1), ("write", 3)]
    ops += [("sync", 1, 3), ("sync", 0, 1), ("sync", 2, 3), ("sync", 0, 2)]
    assert run(n, ops) == 1
