# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scan-algorithm/. The authors are listed in prov/5V7681.jsonl.

import random
from fractions import Fraction

import pytest

from scan_algorithm import DOWN, UP, movement, scan_cost, scan_order, scan_path, scan_simulate

QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]


def runs(path):
    """Number of direction changes along a path of stops."""
    steps = [b - a for a, b in zip(path, path[1:]) if b != a]
    return sum(1 for s, t in zip(steps, steps[1:]) if (s > 0) != (t > 0))


def test_textbook_queue() -> None:
    assert scan_path(QUEUE, 53, DOWN, 200) == [53, 37, 14, 0, 65, 67, 98, 122, 124, 183]
    assert scan_cost(QUEUE, 53, DOWN, 200) == 236
    assert scan_order(QUEUE, 53, UP, 200) == [65, 67, 98, 122, 124, 183, 37, 14]
    assert scan_cost(QUEUE, 53, UP, 200) == 331


def test_edges() -> None:
    assert scan_order([], 5, UP, 10) == []
    assert scan_cost([], 5, UP, 10) == 0
    assert scan_cost([7, 9], 5, UP, 10) == 4  # nothing behind: no trip to the end
    assert scan_cost([3], 5, UP, 10) == 4 + 6  # to cylinder 9, then back to 3
    assert scan_order([5, 5, 4, 6], 5, DOWN, 10) == [5, 5, 4, 6]
    with pytest.raises(ValueError):
        scan_order([10], 5, UP, 10)


def test_invariants_on_random_batches() -> None:
    rng = random.Random(4)
    for _ in range(500):
        c = rng.choice([5, 50, 200])
        req = [rng.randrange(c) for _ in range(rng.randrange(15))]
        head, d = rng.randrange(c), rng.choice([UP, DOWN])
        order = scan_order(req, head, d, c)
        path = scan_path(req, head, d, c)
        assert sorted(order) == sorted(req)
        assert runs(path) <= 1
        assert scan_cost(req, head, d, c) == movement(path)
        behind = [x for x in req if (x - head) * d < 0]
        if behind:
            end = c - 1 if d == UP else 0
            assert scan_cost(req, head, d, c) == abs(end - head) + abs(end - (min(behind) if d == UP else max(behind)))


def test_dynamic_matches_static_batch() -> None:
    rng = random.Random(9)
    for _ in range(200):
        req = [rng.randrange(40) for _ in range(rng.randrange(1, 10))]
        head, d = rng.randrange(40), rng.choice([UP, DOWN])
        fin = scan_simulate([(0, x) for x in req], head, d, 40)
        assert [req[k] for k in sorted(range(len(req)), key=lambda k: fin[k])] == scan_order(req, head, d, 40)
        assert max(fin) == scan_cost(req, head, d, 40)


def test_wait_bound_two_sweeps() -> None:
    c = 200
    for seed in range(3):
        rng = random.Random(seed)
        arrivals = [(t, rng.randrange(c)) for t in range(20000) if rng.random() < 0.05]
        fin = scan_simulate(arrivals, rng.randrange(c), UP, c)
        assert max(f - a for f, (a, _) in zip(fin, arrivals)) <= 2 * (c - 1) - 1


def test_far_request_is_not_starved() -> None:
    for k in (10, 100, 1000):
        arrivals = [(0, 0)] + [(t, 100) for t in range(k)]
        assert scan_simulate(arrivals, 100, UP, 200)[0] == 99 + 199


def test_mean_wait_per_cylinder_in_a_steady_sweep() -> None:
    c = 20
    period = 2 * (c - 1)
    arrivals = [(t, x) for t in range(period) for x in range(c)]
    fin = scan_simulate(arrivals, 0, UP, c)
    for x in range(c):
        waits = [f - a for f, (a, y) in zip(fin, arrivals) if y == x]
        g1, g2 = 2 * x, 2 * (c - 1 - x)
        assert Fraction(sum(waits), period) == Fraction(g1 * g1 + g2 * g2 - period, 2 * period)


def test_arm_sticks_with_positive_service_time() -> None:
    for k in (10, 100, 1000):
        arrivals = [(0, 0)] + [(t, 100) for t in range(k)]
        assert scan_simulate(arrivals, 100, DOWN, 200, service=1)[0] >= k
