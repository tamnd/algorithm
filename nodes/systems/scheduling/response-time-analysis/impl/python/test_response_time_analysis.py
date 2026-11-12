# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/response-time-analysis/. The authors are listed in prov/62Y3C2.jsonl.

import random
from fractions import Fraction

from response_time_analysis import (
    critical_instant_response,
    hyperperiod,
    response_time,
    response_time_analysis,
    schedulable,
    simulate,
)


def random_tasks(rng, n):
    tasks = []
    for _ in range(n):
        t = rng.choice([3, 4, 5, 6, 8, 10, 12, 15, 20])
        c = rng.randint(1, max(1, t // 2))
        tasks.append((c, t, rng.randint(c, t)))
    tasks.sort(key=lambda x: x[2])
    return tasks


def test_example() -> None:
    tasks = [(1, 4, 4), (2, 6, 6), (3, 13, 13)]
    assert response_time_analysis(tasks) == [1, 3, 10]
    assert critical_instant_response(tasks, 2) == 10


def test_miss_and_blocking() -> None:
    assert response_time_analysis([(2, 5, 5), (4, 7, 7)]) == [2, None]
    assert response_time([(1, 4, 4), (2, 6, 6)], 1, blocking=1) == 4
    assert response_time([(1, 4, 4), (2, 6, 6)], 1, blocking=3) is None


def test_against_critical_instant_simulation() -> None:
    rng = random.Random(5)
    checked = 0
    for _ in range(400):
        tasks = random_tasks(rng, rng.randint(1, 4))
        if sum(Fraction(c, t) for c, t, _ in tasks) > 1:
            continue
        for i, r in enumerate(response_time_analysis(tasks)):
            sim = critical_instant_response(tasks, i)
            if r is None:
                assert sim > tasks[i][2]
            else:
                assert r == sim
                checked += 1
    assert checked > 200


def test_critical_instant_is_worst_case() -> None:
    rng = random.Random(9)
    for _ in range(150):
        tasks = random_tasks(rng, 3)
        rs = response_time_analysis(tasks)
        if None in rs:
            continue
        h = hyperperiod(tasks)
        offsets = [rng.randrange(t) for _, t, _ in tasks]
        for task, release, finish in simulate(tasks, offsets, max(offsets) + 2 * h):
            assert finish - release <= rs[task]


def test_fractions() -> None:
    tasks = [(Fraction(1, 2), 2, 2), (Fraction(5, 4), 3, 3)]
    assert response_time_analysis(tasks) == [Fraction(1, 2), Fraction(7, 4)]
    assert schedulable(tasks)
