# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/utilization/. The authors are listed in prov/KNYA42.jsonl.

import random
from fractions import Fraction

from utilization import (completions, fcfs, hyperperiod_demand, littles_law,
                         measured_utilization, number_in_system_area, preemptive_priority,
                         task_set_utilization, utilization_law)

A = [0, 1, 2, 10, 11]
B = [4, 2, 1, 2, 1]


def test_measured_utilization_and_law() -> None:
    s = fcfs(A, B)
    assert measured_utilization(s, 0, 13) == Fraction(10, 13)
    u, x, mean_s = utilization_law(s, completions(s, 5), 0, 13)
    assert (u, x, mean_s) == (Fraction(10, 13), Fraction(5, 13), 2)
    assert u == x * mean_s
    assert measured_utilization(s, 0, 7) == 1


def test_littles_law_example() -> None:
    s = fcfs(A, B)
    c = completions(s, 5)
    assert c == [4, 6, 7, 12, 13]
    big_l, lam, w = littles_law(A, c, 0, 13)
    assert (big_l, lam, w) == (Fraction(18, 13), Fraction(5, 13), Fraction(18, 5))
    assert big_l == lam * w
    # another order changes L and W, not the law
    c2 = completions(preemptive_priority(A, B, [3, 3, 0, 0, 0]), 5)
    big_l2, lam2, w2 = littles_law(A, c2, 0, 13)
    assert big_l2 != big_l and big_l2 == lam2 * w2


def test_littles_law_on_seeded_traces() -> None:
    for seed in range(60):
        rng = random.Random(seed)
        n = rng.randrange(1, 15)
        a = [Fraction(rng.randrange(0, 80), rng.randrange(1, 4)) for _ in range(n)]
        b = [Fraction(rng.randrange(1, 15), rng.randrange(1, 4)) for _ in range(n)]
        prio = [rng.randrange(0, 3) for _ in range(n)]
        for s in (fcfs(a, b), preemptive_priority(a, b, prio)):
            c = completions(s, n)
            t0, t1 = min(a), max(c)  # from the first arrival to the end of the last busy period
            big_l, lam, w = littles_law(a, c, t0, t1)
            assert big_l == lam * w
            assert number_in_system_area(a, c) == sum(ci - ai for ai, ci in zip(a, c))
            # offered load over the interval equals measured utilization
            assert measured_utilization(s, t0, t1) == lam * (sum(b) / n)
            u, x, mean_s = utilization_law(s, c, t0, t1)
            assert u == x * mean_s


def test_task_set_utilization() -> None:
    tasks = [(1, 4), (2, 6), (3, 12)]
    assert task_set_utilization(tasks) == Fraction(5, 6)
    assert hyperperiod_demand(tasks) == (12, 10)
    rng = random.Random(7)
    for _ in range(200):
        k = rng.randrange(1, 6)
        ts = [(rng.randrange(1, 5), rng.randrange(2, 13)) for _ in range(k)]
        h, d = hyperperiod_demand(ts)
        assert d == task_set_utilization(ts) * h


def test_offered_load_queue_example() -> None:
    lam, mean_service = Fraction(4, 5), Fraction(1)
    rho = lam * mean_service
    assert rho == Fraction(4, 5)
    big_l = rho / (1 - rho)  # M/M/1 mean number in system
    assert big_l == 4 and big_l / lam == 5  # W by Little's law
