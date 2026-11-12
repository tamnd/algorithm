# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/work-conserving-scheduling/. The authors are listed in prov/VBE4E8.jsonl.

import random
from fractions import Fraction

from work_conserving_scheduling import (busy_periods, busy_periods_from_trace, nonpreemptive,
                                        preemptive_priority, round_robin, unfinished_work,
                                        waiting_times, work_area)


def all_schedules(a: list, b: list, prio: list, q) -> dict:
    return {
        "fcfs": nonpreemptive(a, b, lambda j: (a[j], j)),
        "lcfs": nonpreemptive(a, b, lambda j: (-a[j], j)),
        "sjf": nonpreemptive(a, b, lambda j: (b[j], a[j], j)),
        "priority": nonpreemptive(a, b, lambda j: (prio[j], a[j], j)),
        "preemptive priority": preemptive_priority(a, b, prio),
        "rr": round_robin(a, b, q),
    }


def trace(rng: random.Random, n: int, exact: bool) -> tuple:
    if exact:
        a = [Fraction(rng.randrange(0, 60), rng.randrange(1, 4)) for _ in range(n)]
        b = [Fraction(rng.randrange(1, 12), rng.randrange(1, 4)) for _ in range(n)]
    else:
        a = [rng.randrange(0, 40) for _ in range(n)]
        b = [rng.randrange(1, 8) for _ in range(n)]
    prio = [rng.randrange(0, 3) for _ in range(n)]
    return a, b, prio


def test_example() -> None:
    a, b, prio = [0, 1, 2, 10, 11], [4, 2, 1, 2, 1], [2, 0, 1, 1, 0]
    expected = [(0, 7), (10, 13)]
    for name, s in all_schedules(a, b, prio, 1).items():
        assert busy_periods(s) == expected, name
    assert busy_periods_from_trace(a, b) == expected


def test_busy_periods_are_invariant_on_seeded_traces() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        a, b, prio = trace(rng, rng.randrange(1, 12), exact=seed % 2 == 0)
        q = Fraction(rng.randrange(1, 4), rng.randrange(1, 3))
        expected = busy_periods_from_trace(a, b)
        for name, s in all_schedules(a, b, prio, q).items():
            assert busy_periods(s) == expected, (seed, name)
            for t in {*a, *(x for _, x, _ in s), *(y for _, _, y in s)}:
                assert unfinished_work(a, b, s, t) == unfinished_work(
                    a, b, all_schedules(a, b, prio, q)["fcfs"], t)


def test_not_work_conserving_differs() -> None:
    a, b = [0, 1], [10, 1]
    idle_first = [(1, 1, 2), (0, 2, 12)]  # waits for the short job
    assert busy_periods(idle_first) == [(1, 12)]
    assert busy_periods_from_trace(a, b) == [(0, 11)]
    lazy = nonpreemptive(a, b, lambda j: (a[j], j), delay=2)
    assert busy_periods(lazy) == [(2, 13)]


def test_sample_path_conservation_law() -> None:
    # For nonpreemptive work-conserving schedulers, the area under the
    # unfinished work equals sum b_j W_j + sum b_j^2 / 2, so sum b_j W_j is
    # the same for all of them. This is the sample-path form of Kleinrock's law.
    for seed in range(40):
        rng = random.Random(100 + seed)
        a, b, prio = trace(rng, rng.randrange(1, 10), exact=True)
        sched = all_schedules(a, b, prio, Fraction(1, 2))
        areas = {name: work_area(s, a, b) for name, s in sched.items()}
        assert len(set(areas.values())) == 1, areas
        weighted = set()
        for name in ("fcfs", "lcfs", "sjf", "priority"):
            w = waiting_times(a, b, sched[name])
            sbw = sum(bj * wj for bj, wj in zip(b, w))
            assert areas[name] == sbw + sum(bj * bj for bj in b) / 2
            weighted.add(sbw)
        assert len(weighted) == 1


def two_machine_list(order: list, burst: list) -> object:
    """Last completion when two machines take the jobs in this order, never idle."""
    free = [0, 0]
    for j in order:
        m = free.index(min(free))
        free[m] += burst[j]
    return max(free)


def test_two_machines_break_the_invariance() -> None:
    b = [4, 1, 1]  # all at time 0; both orders keep the machines busy while jobs wait
    assert two_machine_list([0, 1, 2], b) == 4
    assert two_machine_list([1, 2, 0], b) == 5


def test_mean_wait_is_not_conserved() -> None:
    a, b = [0, 0, 0], [24, 3, 3]
    fcfs = nonpreemptive(a, b, lambda j: (a[j], j))
    sjf = nonpreemptive(a, b, lambda j: (b[j], j))
    assert sum(waiting_times(a, b, fcfs)) == 51
    assert sum(waiting_times(a, b, sjf)) == 9
    # but the burst-weighted sum is
    assert sum(x * y for x, y in zip(b, waiting_times(a, b, fcfs))) == 3 * 24 + 3 * 27
    assert sum(x * y for x, y in zip(b, waiting_times(a, b, sjf))) == 3 * 3 + 24 * 6
