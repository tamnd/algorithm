# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c-look/. The authors are listed in prov/GARAAY.jsonl.

import random

import pytest

from c_look import DOWN, UP, c_look_cost, c_look_order, c_look_simulate, movement

QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]


def c_scan_cost(req, head, d, c):
    ahead = [x for x in req if (x - head) * d >= 0]
    behind = [x for x in req if (x - head) * d < 0]
    if not behind:
        return max((abs(x - head) for x in ahead), default=0)
    end, start = (c - 1, 0) if d == UP else (0, c - 1)
    return abs(end - head) + (c - 1) + max(abs(x - start) for x in behind)


def test_textbook_queue() -> None:
    assert c_look_order(QUEUE, 53, UP, 200) == [65, 67, 98, 122, 124, 183, 14, 37]
    assert c_look_cost(QUEUE, 53, UP, 200) == 322
    assert c_look_cost(QUEUE, 53, UP, 200, count_return=False) == 153
    assert c_look_order(QUEUE, 53, DOWN, 200) == [37, 14, 183, 124, 122, 98, 67, 65]
    assert c_look_cost(QUEUE, 53, DOWN, 200) == 326
    assert c_look_cost(QUEUE, 53, DOWN, 200, count_return=False) == 157


def test_edges() -> None:
    assert c_look_order([], 5, UP, 10) == []
    assert c_look_cost([7, 9], 5, UP, 10) == 4
    assert c_look_cost([1, 3], 5, UP, 10) == 4 + 2  # jump from 5 to 1, then sweep to 3
    assert c_look_cost([1, 3], 5, UP, 10, count_return=False) == 2
    with pytest.raises(ValueError):
        c_look_order([3], 10, UP, 10)


def test_invariants_on_random_batches() -> None:
    rng = random.Random(13)
    for _ in range(500):
        c = rng.choice([5, 50, 200])
        req = [rng.randrange(c) for _ in range(rng.randrange(15))]
        head, d = rng.randrange(c), rng.choice([UP, DOWN])
        order = c_look_order(req, head, d, c)
        assert sorted(order) == sorted(req)
        assert sum(1 for a, b in zip(order, order[1:]) if (b - a) * d < 0) <= 1
        cost = c_look_cost(req, head, d, c)
        assert cost == movement([head, *order])
        assert cost <= c_scan_cost(req, head, d, c)
        assert c_look_cost(req, head, d, c, count_return=False) <= cost


def test_dynamic_matches_static_batch() -> None:
    rng = random.Random(14)
    for _ in range(200):
        req = [rng.randrange(40) for _ in range(rng.randrange(1, 10))]
        head, d = rng.randrange(40), rng.choice([UP, DOWN])
        fin = c_look_simulate([(0, x) for x in req], head, d, 40)
        assert [req[k] for k in sorted(range(len(req)), key=lambda k: fin[k])] == c_look_order(req, head, d, 40)
        assert max(fin) == c_look_cost(req, head, d, 40)


def test_wait_bound() -> None:
    c = 200
    worst = 0
    for seed in range(3):
        rng = random.Random(seed)
        arrivals = [(t, rng.randrange(c)) for t in range(20000) if rng.random() < 0.05]
        fin = c_look_simulate(arrivals, rng.randrange(c), UP, c)
        worst = max(worst, max(f - a for f, (a, _) in zip(fin, arrivals)))
    assert 2 * (c - 1) < worst <= 3 * (c - 1)


def test_request_that_arrives_during_the_jump() -> None:
    # The head jumps from 199 to 10 during ticks 0 to 189. Requests at 5 and 198 arrive at tick 1.
    # The head lands at 10, sweeps up to 198, and jumps back to 5: about three sweeps.
    arrivals = [(0, 199), (0, 10), (1, 5), (1, 198)]
    fin = c_look_simulate(arrivals, 199, UP, 200)
    assert fin == [0, 189, 189 + 188 + 193, 189 + 188]
    assert fin[2] - 1 == 569 > 2 * (200 - 1)
