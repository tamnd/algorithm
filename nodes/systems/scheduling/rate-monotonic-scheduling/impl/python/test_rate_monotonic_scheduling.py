# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rate-monotonic-scheduling/. The authors are listed in prov/JM2GFC.jsonl.

import itertools
import random
from fractions import Fraction

from rate_monotonic_scheduling import (
    fixed_priority_schedule,
    hyperbolic_test,
    hyperperiod,
    liu_layland_test,
    rate_monotonic_order,
    rate_monotonic_scheduling,
    simulation_test,
    utilization,
)


def random_tasks(rng, n, periods=(2, 3, 4, 5, 6, 8, 10, 12, 15, 20)):
    tasks = []
    for _ in range(n):
        t = rng.choice(periods)
        tasks.append((rng.randint(1, t), t))
    return tasks


def test_example_trace() -> None:
    tasks = [(1, 4), (2, 6), (3, 12)]
    pieces, missed = rate_monotonic_scheduling(tasks)
    assert missed == []
    assert pieces == [(0, 1, 0), (1, 3, 1), (3, 4, 2), (4, 5, 0), (5, 6, 2), (6, 8, 1), (8, 9, 0), (9, 10, 2)]
    assert utilization(tasks) == Fraction(5, 6)
    assert not liu_layland_test(tasks) and not hyperbolic_test(tasks)


def test_order_and_hyperperiod() -> None:
    assert rate_monotonic_order([(1, 6), (1, 4), (1, 6), (1, 2)]) == [3, 1, 0, 2]
    assert hyperperiod([(1, 4), (1, 6), (1, 10)]) == 60


def test_miss_below_one() -> None:
    _, missed = rate_monotonic_scheduling([(2, 5), (4, 7)])
    assert missed and missed[0] == (1, 0)


def test_bounds_are_sufficient_not_necessary() -> None:
    assert simulation_test([(1, 2), (2, 4)]) and not hyperbolic_test([(1, 2), (2, 4)])
    both = [(3, 5), (1, 4)]
    assert hyperbolic_test(both) and not liu_layland_test(both) and simulation_test(both)


def test_liu_layland_exact_edge() -> None:
    assert liu_layland_test([(1, 1)])
    assert not liu_layland_test([(1, 1), (Fraction(1, 1000), 1)])
    assert liu_layland_test([(Fraction(828, 1000), 1), (0, 1)])
    assert not liu_layland_test([(Fraction(829, 1000), 1), (0, 1)])


def test_bounds_against_simulation() -> None:
    rng = random.Random(7)
    seen = {"ll": 0, "hyp_only": 0, "sim_only": 0}
    for _ in range(1500):
        tasks = random_tasks(rng, rng.randint(2, 4))
        if utilization(tasks) > 1:
            continue
        ll, hyp, sim = liu_layland_test(tasks), hyperbolic_test(tasks), simulation_test(tasks)
        assert not ll or hyp
        assert not hyp or sim
        seen["ll"] += ll
        seen["hyp_only"] += hyp and not ll
        seen["sim_only"] += sim and not hyp
    assert min(seen.values()) > 0


def test_rm_optimal_among_fixed_priorities() -> None:
    rng = random.Random(11)
    for _ in range(300):
        tasks = random_tasks(rng, rng.randint(2, 4), periods=(2, 3, 4, 6, 8, 12))
        if utilization(tasks) > 1:
            continue
        some = any(simulation_test(tasks, list(p)) for p in itertools.permutations(range(len(tasks))))
        assert simulation_test(tasks) == some


def test_schedule_is_valid() -> None:
    rng = random.Random(3)
    for _ in range(100):
        tasks = random_tasks(rng, 3)
        h = hyperperiod(tasks)
        pieces, jobs = fixed_priority_schedule(tasks, rate_monotonic_order(tasks), h)
        for (a, b, _), (c, _, _) in zip(pieces, pieces[1:]):
            assert a < b <= c
        done = {}
        for a, b, i in pieces:
            done[i] = done.get(i, 0) + (b - a)
        assert all(done.get(i, 0) == tasks[i][0] * len([j for j in jobs if j["task"] == i]) for i in range(3))


def test_fractions() -> None:
    tasks = [(Fraction(1, 2), 2), (Fraction(3, 2), 3)]
    pieces, missed = rate_monotonic_scheduling(tasks)
    assert missed == []
    assert pieces[0] == (0, Fraction(1, 2), 0)
