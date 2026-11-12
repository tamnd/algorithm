# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earliest-deadline-first/. The authors are listed in prov/20A95V.jsonl.

import random
from fractions import Fraction

from earliest_deadline_first import (
    demand_bound,
    earliest_deadline_first,
    edf_jobs,
    global_edf,
    hyperperiod,
    processor_demand_test,
    utilization,
)


def slot_feasible(jobs):
    """Brute force for integer jobs: try every choice of job in every unit slot."""
    end = max(d for _, _, d in jobs)
    states = {tuple(w for _, w, _ in jobs)}
    for t in range(end):
        new = set()
        for s in states:
            choices = [k for k in range(len(jobs)) if jobs[k][0] <= t and s[k] > 0]
            for k in choices or [None]:
                n = list(s)
                if k is not None:
                    n[k] -= 1
                if all(n[j] == 0 or jobs[j][2] > t + 1 for j in range(len(jobs))):
                    new.add(tuple(n))
        states = new
    return any(all(x == 0 for x in s) for s in states)


def test_example() -> None:
    pieces, missed = earliest_deadline_first([(2, 5), (4, 7)])
    assert missed == []
    assert pieces[:5] == [(0, 2, 0), (2, 6, 1), (6, 8, 0), (8, 12, 1), (12, 14, 0)]


def test_job_set() -> None:
    jobs = [(0, 3, 7), (1, 2, 4), (2, 1, 5)]
    pieces, finish = edf_jobs(jobs)
    assert pieces == [(0, 1, 0), (1, 3, 1), (3, 4, 2), (4, 6, 0)]
    assert finish == [6, 3, 4]


def test_edf_meets_deadlines_when_feasible() -> None:
    rng = random.Random(2)
    feasible = 0
    for _ in range(400):
        jobs = []
        for _ in range(rng.randint(1, 4)):
            r = rng.randint(0, 5)
            w = rng.randint(1, 3)
            jobs.append((r, w, r + w + rng.randint(0, 4)))
        _, finish = edf_jobs(jobs)
        ok = all(f <= d for f, (_, _, d) in zip(finish, jobs))
        assert ok == slot_feasible(jobs)
        feasible += ok
    assert 50 < feasible < 400


def test_implicit_deadlines_utilization_test() -> None:
    rng = random.Random(4)
    for _ in range(300):
        tasks = []
        for _ in range(rng.randint(1, 4)):
            t = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
            tasks.append((rng.randint(1, t), t))
        _, missed = earliest_deadline_first(tasks)
        assert (missed == []) == (utilization(tasks) <= 1)


def test_processor_demand_against_simulation() -> None:
    rng = random.Random(8)
    yes = no = 0
    for _ in range(500):
        tasks = []
        for _ in range(rng.randint(1, 4)):
            t = rng.choice([3, 4, 5, 6, 8, 10, 12])
            c = rng.randint(1, t // 2 + 1)
            tasks.append((c, t, rng.randint(c, t)))
        _, missed = earliest_deadline_first(tasks)
        verdict = processor_demand_test(tasks)
        assert verdict == (missed == [])
        yes += verdict
        no += not verdict
    assert yes > 50 and no > 50


def test_constrained_example() -> None:
    tasks = [(2, 4, 2), (2, 6, 3)]
    assert utilization(tasks) == Fraction(5, 6)
    assert demand_bound(tasks, 3) == 4
    assert not processor_demand_test(tasks)
    assert processor_demand_test([(1, 4, 2), (2, 6, 4), (3, 12, 9)])


def test_dhall_effect() -> None:
    jobs = [(0, 2, 10), (0, 2, 10), (0, 10, 11)]
    assert global_edf(jobs, 2) == [2, 2, 12]
    assert edf_jobs(jobs[:2])[1] == [2, 4] and edf_jobs(jobs[2:])[1] == [10]
    assert hyperperiod([(2, 10), (2, 10), (10, 11)]) == 110
