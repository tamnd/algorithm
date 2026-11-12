# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/look/. The authors are listed in prov/6RZ6QE.jsonl.

import random
from itertools import permutations

import pytest

from look import DOWN, UP, look_cost, look_order, look_simulate, movement, offline_optimum

QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]


def scan_cost(req, head, d, c):
    ahead = [x for x in req if (x - head) * d >= 0]
    behind = [x for x in req if (x - head) * d < 0]
    if not behind:
        return max((abs(x - head) for x in ahead), default=0)
    end = c - 1 if d == UP else 0
    return abs(end - head) + max(abs(end - x) for x in behind)


def best(req, head):
    return min(movement([head, *p]) for p in permutations(req))


def test_textbook_queue() -> None:
    assert look_order(QUEUE, 53, DOWN, 200) == [37, 14, 65, 67, 98, 122, 124, 183]
    assert look_cost(QUEUE, 53, DOWN, 200) == 208
    assert look_cost(QUEUE, 53, UP, 200) == 299
    assert offline_optimum(QUEUE, 53) == 208 == best(QUEUE, 53)


def test_edges() -> None:
    assert look_order([], 5, UP, 10) == []
    assert look_cost([3], 5, UP, 10) == 2  # nothing ahead: turn at once
    assert look_cost([7, 9], 5, DOWN, 10) == 4
    with pytest.raises(ValueError):
        look_order([3], 5, 2, 10)


def test_optimal_when_it_starts_toward_the_nearer_end() -> None:
    rng = random.Random(21)
    for _ in range(300):
        c = rng.choice([10, 100])
        req = [rng.randrange(c) for _ in range(rng.randrange(1, 8))]
        head = rng.randrange(c)
        lo, hi = min(req), max(req)
        d = DOWN if head - lo <= hi - head else UP
        assert look_cost(req, head, d, c) == offline_optimum(req, head) == best(req, head)
        for d in (UP, DOWN):
            order = look_order(req, head, d, c)
            assert sorted(order) == sorted(req)
            assert look_cost(req, head, d, c) <= scan_cost(req, head, d, c)
            steps = [b - a for a, b in zip([head, *order], order) if b != a]
            assert sum(1 for s, t in zip(steps, steps[1:]) if (s > 0) != (t > 0)) <= 1


def test_dynamic_matches_static_batch() -> None:
    rng = random.Random(6)
    for _ in range(200):
        req = [rng.randrange(40) for _ in range(rng.randrange(1, 10))]
        head, d = rng.randrange(40), rng.choice([UP, DOWN])
        fin = look_simulate([(0, x) for x in req], head, d, 40)
        assert [req[k] for k in sorted(range(len(req)), key=lambda k: fin[k])] == look_order(req, head, d, 40)
        assert max(fin) == look_cost(req, head, d, 40)


def test_wait_bound_and_no_starvation() -> None:
    c = 200
    for seed in range(3):
        rng = random.Random(seed)
        arrivals = [(t, rng.randrange(c)) for t in range(20000) if rng.random() < 0.05]
        fin = look_simulate(arrivals, rng.randrange(c), UP, c)
        assert max(f - a for f, (a, _) in zip(fin, arrivals)) <= 2 * (c - 1) - 1
    for k in (10, 100, 1000):
        arrivals = [(0, 0)] + [(t, 100) for t in range(k)]
        assert look_simulate(arrivals, 100, UP, 200)[0] == 100
