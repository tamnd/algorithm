# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/last-writer-wins/. The authors are listed in prov/SZ23RT.jsonl.

import random
from itertools import permutations

from last_writer_wins import Net, Replica, concurrent_run, lww_merge, skew_run


def test_merge_is_commutative_associative_idempotent() -> None:
    ws = [((5, 0), "x"), ((5, 1), "y"), ((3, 2), "z"), None]
    for a in ws:
        assert lww_merge(a, a) == a
        for b in ws:
            assert lww_merge(a, b) == lww_merge(b, a)
            for c in ws:
                assert lww_merge(lww_merge(a, b), c) == lww_merge(a, lww_merge(b, c))


def test_tie_broken_by_replica_id() -> None:
    assert lww_merge(((5, 0), "x"), ((5, 1), "y")) == ((5, 1), "y")


def test_concurrent_write_is_lost() -> None:
    reps = concurrent_run()
    vals = {r.value() for r in reps}
    assert vals == {"cart = {pen}"}  # same timestamp 10, replica 1 has the larger id
    # the other write left no trace at any replica
    assert all(r.cell[1] != "cart = {book}" for r in reps)


def test_skewed_clock_overrides_a_later_write() -> None:
    reps = skew_run("physical")
    # "b" was written after its writer had seen "a", but "a" has stamp 110 > 20
    assert [r.value() for r in reps] == ["a", "a"]
    reps = skew_run("lamport")
    assert [r.value() for r in reps] == ["b", "b"]


def test_converges_in_any_delivery_order() -> None:
    for seed in range(300):
        rng = random.Random(seed)
        n = rng.randint(2, 5)
        reps = [Replica(i, skew=rng.randint(-50, 50)) for i in range(n)]
        net = Net(reps, seed)
        for k in range(rng.randint(1, 8)):
            net.write(rng.randrange(n), f"v{k}", rng.randint(0, 100))
        net.run()
        cells = {r.cell for r in reps}
        assert len(cells) == 1


def test_order_of_merges_does_not_matter() -> None:
    ws = [((3, 0), "a"), ((7, 2), "b"), ((7, 1), "c"), ((1, 3), "d")]
    results = set()
    for order in permutations(ws):
        cell = None
        for w in order:
            cell = lww_merge(cell, w)
        results.add(cell)
    assert results == {((7, 2), "b")}
