# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shortest-seek-time-first/. The authors are listed in prov/PME9E7.jsonl.

import random
from itertools import permutations

import pytest

from shortest_seek_time_first import DOWN, UP, head_movement, sstf_cost, sstf_order, sstf_simulate

QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]


def naive_sstf(requests, head, d):
    """Pick the nearest pending request each time; ties go in the direction of the last move."""
    rest, p, out = list(requests), head, []
    while rest:
        m = min(abs(x - p) for x in rest)
        near = [x for x in rest if abs(x - p) == m]
        x = next((y for y in near if (y - p) * d > 0), near[0])
        if x != p:
            d = UP if x > p else DOWN
        rest.remove(x)
        out.append(x)
        p = x
    return out


def test_textbook_queue() -> None:
    for d in (UP, DOWN):
        assert sstf_order(QUEUE, 53, d, 200) == [65, 67, 37, 14, 98, 122, 124, 183]
        assert sstf_cost(QUEUE, 53, d, 200) == 236
    assert min(head_movement(p, 53) for p in permutations(QUEUE)) == 208


def test_not_optimal_small() -> None:
    assert sstf_order([46, 53, 58], 50, UP, 100) == [53, 58, 46]
    assert sstf_cost([46, 53, 58], 50, UP, 100) == 20
    assert min(head_movement(p, 50) for p in permutations([46, 53, 58])) == 16
    for q in (3, 50, 500):  # a chain of steps of 2 pulls SSTF away from 8; the ratio tends to 2
        chain = [11 + 2 * k for k in range(q)]
        top = chain[-1]
        assert sstf_order([8, *chain], 10, UP, 2000) == [*chain, 8]
        assert sstf_cost([8, *chain], 10, UP, 2000) == 2 * top - 18
        best = (top - 8) + min(10 - 8, top - 10)
        assert best == top - 6
        if q == 3:
            assert min(head_movement(p, 10) for p in permutations([8, *chain])) == best


def test_tie_rule() -> None:
    assert sstf_order([40, 60], 50, UP, 100) == [60, 40]
    assert sstf_order([40, 60], 50, DOWN, 100) == [40, 60]
    assert sstf_order([11, 9, 7, 13], 10, DOWN, 100) == [9, 7, 11, 13]
    assert sstf_order([11, 9, 7, 13], 10, UP, 100) == [11, 13, 9, 7]


def test_against_naive_and_invariants() -> None:
    rng = random.Random(11)
    for _ in range(500):
        c = rng.choice([8, 30, 200])
        req = [rng.randrange(c) for _ in range(rng.randrange(12))]
        head, d = rng.randrange(c), rng.choice([UP, DOWN])
        order = sstf_order(req, head, d, c)
        assert order == naive_sstf(req, head, d)
        assert sorted(order) == sorted(req)
        p = head
        for k, x in enumerate(order):  # each step goes to a nearest pending request
            assert all(abs(x - p) <= abs(y - p) for y in order[k:])
            seen = order[: k + 1]  # the served requests form a run of the sorted batch
            lo, hi = min(seen), max(seen)
            assert sum(lo < y < hi for y in seen) == sum(lo < y < hi for y in req)
            p = x


def test_dynamic_matches_static_batch() -> None:
    rng = random.Random(3)
    for _ in range(200):
        req = [rng.randrange(60) for _ in range(rng.randrange(1, 10))]
        head, d = rng.randrange(60), rng.choice([UP, DOWN])
        fin = sstf_simulate([(0, x) for x in req], head, d, 60)
        by_finish = [req[k] for k in sorted(range(len(req)), key=lambda k: fin[k])]
        assert by_finish == sstf_order(req, head, d, 60)
        assert max(fin) == sstf_cost(req, head, d, 60)


def test_starvation_grows_with_the_stream() -> None:
    waits = []
    for k in (10, 100, 1000):
        arrivals = [(0, 0)] + [(t, 100) for t in range(k)]
        fin = sstf_simulate(arrivals, 100, UP, 200)
        waits.append(fin[0])
        assert fin[0] >= k
    assert waits == [110, 200, 1100]  # k + 100: the far request waits for the whole stream
    rng = random.Random(8)
    for k in (100, 1000):
        arrivals = [(0, 0)] + [(t, rng.randrange(95, 106)) for t in range(k)]
        assert sstf_simulate(arrivals, 100, UP, 200)[0] >= k


def test_dynamic_random_stream() -> None:
    rng = random.Random(7)
    arrivals = [(t, rng.randrange(200)) for t in range(5000) if rng.random() < 0.05]
    fin = sstf_simulate(arrivals, 100, UP, 200, service=2)
    assert all(f >= a + 2 for f, (a, _) in zip(fin, arrivals))


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        sstf_order([200], 0, UP, 200)
    with pytest.raises(ValueError):
        sstf_order([1], 0, 0, 200)
