# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deadline-monotonic-scheduling/. The authors are listed in prov/RQ7EFJ.jsonl.

import itertools
import random
from fractions import Fraction
from math import lcm

from deadline_monotonic_scheduling import (
    audsley_optimal_priority_assignment,
    deadline_monotonic_order,
    deadline_monotonic_scheduling,
    simulate,
    worst_response_time,
)


def feasible(tasks, order):
    """Reference: simulate synchronous release; jobs of [0, H) must meet their deadlines."""
    if sum(Fraction(c, t) for c, t, _ in tasks) > 1:
        return False
    h = lcm(*(t for _, t, _ in tasks))
    return all(f - r <= tasks[i][2] for i, r, f in simulate(tasks, order, 2 * h) if r < h)


def random_tasks(rng, n, factor):
    tasks = []
    for _ in range(n):
        t = rng.choice([2, 3, 4, 5, 6, 8, 12])
        c = rng.randint(1, max(1, t // 2))
        tasks.append((c, t, rng.randint(c, factor * t)))
    return tasks


def test_example_dm_beats_rm() -> None:
    tasks = [(2, 10, 2), (1, 5, 5)]
    assert deadline_monotonic_order(tasks) == [0, 1]
    assert deadline_monotonic_scheduling(tasks) == []
    assert not feasible(tasks, [1, 0])


def test_dm_optimal_for_constrained_deadlines() -> None:
    rng = random.Random(12)
    hits = 0
    for _ in range(400):
        tasks = random_tasks(rng, rng.randint(2, 4), 1)
        some = any(feasible(tasks, list(p)) for p in itertools.permutations(range(len(tasks))))
        assert feasible(tasks, deadline_monotonic_order(tasks)) == some
        hits += some
    assert hits > 30


def test_dm_not_optimal_for_long_deadlines() -> None:
    tasks = [(2, 4, 6), (4, 8, 7)]
    assert not feasible(tasks, deadline_monotonic_order(tasks))
    assert audsley_optimal_priority_assignment(tasks) == [1, 0]
    assert feasible(tasks, [1, 0])


def test_busy_period_response_time_against_simulation() -> None:
    rng = random.Random(3)
    for _ in range(300):
        tasks = random_tasks(rng, rng.randint(1, 3), 3)
        if sum(Fraction(c, t) for c, t, _ in tasks) > 1:
            continue
        h = lcm(*(t for _, t, _ in tasks))
        order = list(range(len(tasks)))
        out = simulate(tasks, order, 2 * h)
        for i in order:
            worst = max(f - r for j, r, f in out if j == i and r < h)
            assert worst_response_time(tasks, i, order[:i]) == worst


def test_audsley_against_brute_force() -> None:
    rng = random.Random(21)
    found = 0
    for _ in range(400):
        tasks = random_tasks(rng, rng.randint(2, 4), 2)
        some = any(feasible(tasks, list(p)) for p in itertools.permutations(range(len(tasks))))
        order = audsley_optimal_priority_assignment(tasks)
        assert (order is not None) == some
        if order is not None:
            assert feasible(tasks, order)
            found += 1
    assert found > 30
