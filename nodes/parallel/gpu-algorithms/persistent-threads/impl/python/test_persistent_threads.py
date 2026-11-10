# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/persistent-threads/. The authors are listed in prov/NMFBCT.jsonl.
import random
from fractions import Fraction as F

import pytest

from persistent_threads import (
    Deadlock, graham_bound, grid_barrier_run, max_persistent_blocks, persistent_queue, rounds_time,
    static_blocks,
)


def test_every_task_once_and_atomic_count():
    rng = random.Random(5)
    for _ in range(100):
        n = rng.randrange(0, 200)
        p = rng.randrange(1, 9)
        g = rng.choice([1, 4, 32])
        costs = [rng.randrange(1, 20) for _ in range(n)]
        span, atomics, owner = persistent_queue(costs, p, g, fetch_cost=1)
        assert all(o is not None for o in owner)
        assert atomics == -(-n // g) + p          # one fetch per batch, one failed fetch per worker
        assert span <= graham_bound(costs, p, g, fetch_cost=1)
        assert span >= F(sum(costs), p)


def test_worked_example_skewed_costs():
    # 8 tasks, 2 workers; the expensive tasks are all in the first half
    costs = [10, 10, 10, 10, 1, 1, 1, 1]
    assert static_blocks(costs, 2) == 40
    span, atomics, _ = persistent_queue(costs, 2)
    assert span == 22 and atomics == 10
    span4, atomics4, _ = persistent_queue(costs, 2, batch=4)
    assert span4 == 40 and atomics4 == 4


def test_rounds_model():
    # assumed: 1000 rounds of 10 us; launch 5 us; grid barrier 2 us
    assert rounds_time(1000, 10, 5, 2, persistent=False) == 15000
    assert rounds_time(1000, 10, 5, 2, persistent=True) == 12005


def test_grid_barrier_needs_co_residency():
    assert grid_barrier_run(8, 8) == list(range(8))
    with pytest.raises(Deadlock):
        grid_barrier_run(9, 8)
    assert max_persistent_blocks(80, 2) == 160   # assumed: 80 SMs, 2 resident blocks per SM
    grid_barrier_run(160, max_persistent_blocks(80, 2))
    with pytest.raises(Deadlock):
        grid_barrier_run(161, max_persistent_blocks(80, 2))
