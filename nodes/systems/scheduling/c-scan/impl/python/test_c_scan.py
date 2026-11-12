# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c-scan/. The authors are listed in prov/PAACQ9.jsonl.

import random
from fractions import Fraction

import pytest

from c_scan import DOWN, UP, c_scan_cost, c_scan_order, c_scan_path, c_scan_simulate, movement

QUEUE = [98, 183, 37, 122, 14, 124, 65, 67]


def test_textbook_queue() -> None:
    assert c_scan_path(QUEUE, 53, UP, 200) == [53, 65, 67, 98, 122, 124, 183, 199, 0, 14, 37]
    assert c_scan_cost(QUEUE, 53, UP, 200) == 382
    assert c_scan_cost(QUEUE, 53, UP, 200, count_return=False) == 183
    assert c_scan_order(QUEUE, 53, DOWN, 200) == [37, 14, 183, 124, 122, 98, 67, 65]
    assert c_scan_cost(QUEUE, 53, DOWN, 200) == 386
    assert c_scan_cost(QUEUE, 53, DOWN, 200, count_return=False) == 187


def test_edges() -> None:
    assert c_scan_order([], 5, UP, 10) == []
    assert c_scan_cost([7, 9], 5, UP, 10) == 4
    assert c_scan_cost([3], 5, UP, 10) == 4 + 9 + 3
    assert c_scan_cost([3], 5, UP, 10, count_return=False) == 4 + 3
    with pytest.raises(ValueError):
        c_scan_order([-1], 5, UP, 10)


def test_invariants_on_random_batches() -> None:
    rng = random.Random(12)
    for _ in range(500):
        c = rng.choice([5, 50, 200])
        req = [rng.randrange(c) for _ in range(rng.randrange(15))]
        head, d = rng.randrange(c), rng.choice([UP, DOWN])
        order = c_scan_order(req, head, d, c)
        assert sorted(order) == sorted(req)
        # each sweep is monotone in the service direction, with at most one wrap
        wraps = sum(1 for a, b in zip(order, order[1:]) if (b - a) * d < 0)
        assert wraps <= 1
        path = c_scan_path(req, head, d, c)
        assert c_scan_cost(req, head, d, c) == movement(path)
        if any((x - head) * d < 0 for x in req):
            assert c_scan_cost(req, head, d, c) - c_scan_cost(req, head, d, c, False) == c - 1


def test_dynamic_matches_static_batch() -> None:
    rng = random.Random(10)
    for _ in range(200):
        req = [rng.randrange(40) for _ in range(rng.randrange(1, 10))]
        head, d = rng.randrange(40), rng.choice([UP, DOWN])
        fin = c_scan_simulate([(0, x) for x in req], head, d, 40)
        assert [req[k] for k in sorted(range(len(req)), key=lambda k: fin[k])] == c_scan_order(req, head, d, 40)
        assert max(fin) == c_scan_cost(req, head, d, 40)


def test_wait_bound() -> None:
    c = 200
    for seed, r in ((0, None), (1, 10), (2, 0)):
        rng = random.Random(seed)
        arrivals = [(t, rng.randrange(c)) for t in range(20000) if rng.random() < 0.05]
        fin = c_scan_simulate(arrivals, rng.randrange(c), UP, c, return_ticks=r)
        bound = (c - 1) + (c - 1 if r is None else r)
        assert max(f - a for f, (a, _) in zip(fin, arrivals)) <= bound


def test_mean_wait_is_the_same_on_every_cylinder() -> None:
    c = 20
    for r in (None, 3):
        period = (c - 1) + (c - 1 if r is None else r)
        arrivals = [(t, x) for t in range(period) for x in range(c)]
        fin = c_scan_simulate(arrivals, 0, UP, c, return_ticks=r)
        for x in range(c):
            waits = [f - a for f, (a, y) in zip(fin, arrivals) if y == x]
            assert sorted(waits) == list(range(period))
            assert Fraction(sum(waits), period) == Fraction(period - 1, 2)
