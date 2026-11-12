# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-problem/. The authors are listed in prov/X20JQV.jsonl.

import random

from scheduling_problem import (Job, OBJECTIVES, best_nonpreemptive, completion_times,
                                is_feasible, schedule_order)

EXAMPLE = [Job(0, 4, 6, 1), Job(1, 2, 4, 3), Job(2, 1, 5, 1), Job(3, 3, 12, 2)]


def test_example_optima() -> None:
    assert best_nonpreemptive(EXAMPLE, "Cmax") == (10, [0, 1, 2, 3])
    assert best_nonpreemptive(EXAMPLE, "sumC") == (25, [1, 2, 3, 0])
    assert best_nonpreemptive(EXAMPLE, "sumwC") == (38, [1, 2, 3, 0])
    assert best_nonpreemptive(EXAMPLE, "sumF") == (19, [1, 2, 3, 0])
    assert best_nonpreemptive(EXAMPLE, "Lmax")[0] == 2
    assert best_nonpreemptive(EXAMPLE, "sumU")[0] == 1


def test_example_fcfs_order() -> None:
    c = completion_times(EXAMPLE, schedule_order(EXAMPLE, [0, 1, 2, 3]))
    assert c == [4, 6, 7, 10]
    assert OBJECTIVES["sumC"](EXAMPLE, c) == 27


def test_example_preemptive() -> None:
    pieces = [(0, 0, 1, 0), (0, 1, 3, 1), (0, 3, 4, 2), (0, 4, 7, 0), (0, 7, 10, 3)]
    assert is_feasible(EXAMPLE, pieces, preemptive=True)
    assert not is_feasible(EXAMPLE, pieces, preemptive=False)
    assert sum(completion_times(EXAMPLE, pieces)) == 24


def test_checker_rejects() -> None:
    ok = schedule_order(EXAMPLE, [0, 1, 2, 3])
    assert is_feasible(EXAMPLE, ok)
    assert not is_feasible(EXAMPLE, [(0, 0, 4, 0), (0, 0, 2, 1), (0, 6, 7, 2), (0, 7, 10, 3)])
    assert not is_feasible(EXAMPLE, [(0, 0, 4, 0), (0, 0, 2, 1), (0, 4, 5, 2), (0, 7, 10, 3)])
    assert not is_feasible(EXAMPLE, ok[:3])
    two = [(0, 0, 4, 0), (1, 1, 3, 1), (1, 3, 4, 2), (1, 4, 7, 3)]
    assert is_feasible(EXAMPLE, two, machines=2)
    assert not is_feasible(EXAMPLE, two, machines=1)


def test_rules_at_time_zero() -> None:
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randrange(1, 6)
        jobs = [Job(0, rng.randrange(1, 9), rng.randrange(0, 20), rng.randrange(1, 5)) for _ in range(n)]
        spt = sorted(range(n), key=lambda j: jobs[j].p)
        edd = sorted(range(n), key=lambda j: jobs[j].d)
        smith = sorted(range(n), key=lambda j: jobs[j].p / jobs[j].w)
        val = lambda o, order: OBJECTIVES[o](jobs, completion_times(jobs, schedule_order(jobs, order)))
        assert best_nonpreemptive(jobs, "sumC")[0] == val("sumC", spt)
        assert best_nonpreemptive(jobs, "Lmax")[0] == val("Lmax", edd)
        assert best_nonpreemptive(jobs, "sumwC")[0] == val("sumwC", smith)
        assert best_nonpreemptive(jobs, "Cmax")[0] == sum(j.p for j in jobs)
