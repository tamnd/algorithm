# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-misra-bryant/. The authors are listed in prov/ASK6PS.jsonl.

import random

from chandy_misra_bryant import CMB, sequential


def random_network(rng: random.Random, n: int) -> list[list[int]]:
    # A ring makes the graph strongly connected; add a few random links.
    outs = [{(i + 1) % n} for i in range(n)]
    for _ in range(n):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            outs[a].add(b)
    return [sorted(o) for o in outs]


def test_matches_sequential_simulation() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        n = rng.randrange(2, 7)
        outs = random_network(rng, n)
        start = [rng.randrange(n) for _ in range(rng.randrange(1, 8))]
        L = rng.randrange(1, 4)
        cmb = CMB(outs, start, L, end=50, seed=seed)
        assert cmb.run() == "done"
        assert cmb.result() == sequential(outs, start, L, 50)


# The page example: links 0 -> 1, 1 -> 0, 0 -> 2, 2 -> 0, and one job that
# starts at station 0 and goes to station 1 on its first visit.
OUTS = [[1, 2], [0], [0]]


def test_page_example_deadlock_without_nulls() -> None:
    blocked = CMB(OUTS, [0], 1, end=30, seed=1, nulls=False)
    assert blocked.run() == "deadlock"
    # Station 0 holds the job back from station 1 at time 3, because the
    # link from station 2 may still bring an earlier job.
    assert blocked.result() == [[(0, -1, 0)], [(1, 0, 0)], []]
    assert list(blocked.st[0].queue[1]) == [(3, 1, 0, 2)]


def test_page_example_with_nulls() -> None:
    ok = CMB(OUTS, [0], 1, end=30, seed=1, nulls=True)
    assert ok.run() == "done"
    assert ok.result() == sequential(OUTS, [0], 1, 30)
    assert [len(x) for x in ok.result()] == [7, 6, 0]
    assert ok.null_count > 0


def test_every_network_deadlocks_or_matches_without_nulls() -> None:
    # Without nulls a run either matches the sequential result or stops early.
    for seed in range(20):
        rng = random.Random(seed)
        n = rng.randrange(2, 6)
        outs = random_network(rng, n)
        start = [rng.randrange(n) for _ in range(3)]
        cmb = CMB(outs, start, 1, end=40, seed=seed, nulls=False)
        want = sequential(outs, start, 1, 40)
        if cmb.run() == "done":
            assert cmb.result() == want
        else:
            assert all(got == w[: len(got)] for got, w in zip(cmb.result(), want))


def test_page_example_zero_lookahead_deadlocks() -> None:
    # With L = 0 the nulls on the cycle 0 -> 2 -> 0 stop growing.
    zero = CMB(OUTS, [0], 0, end=30, seed=1, nulls=True)
    assert zero.run() == "deadlock"
