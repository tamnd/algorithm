# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backfilling/. The authors are listed in prov/ARFFDA.jsonl.

import random

import pytest

from backfilling import Job, backfill, earliest_fit

EXAMPLE = [
    Job("J1", 0, 2, 10, 10),
    Job("J2", 1, 3, 5, 5),
    Job("J3", 2, 4, 5, 5),
    Job("J4", 3, 1, 20, 20),
    Job("J5", 4, 2, 5, 5),
]


def test_example() -> None:
    fcfs = backfill(4, EXAMPLE, "fcfs")
    assert fcfs.start == {"J1": 0, "J2": 10, "J3": 15, "J4": 20, "J5": 20}
    easy = backfill(4, EXAMPLE, "easy")
    assert easy.start == {"J1": 0, "J4": 3, "J2": 10, "J5": 15, "J3": 23}
    assert easy.reservation["J2"] == 10 and easy.reservation["J3"] == 23
    cons = backfill(4, EXAMPLE, "conservative")
    assert cons.start == {"J1": 0, "J5": 4, "J2": 10, "J3": 15, "J4": 20}
    assert cons.reservation == {"J1": 0, "J2": 10, "J3": 15, "J4": 20, "J5": 4}


def test_early_end_compresses_conservative_schedule() -> None:
    jobs = [Job("J1", 0, 2, 10, 6)] + EXAMPLE[1:]  # J1 ends at 6, not 10
    cons = backfill(4, jobs, "conservative")
    assert cons.start == {"J1": 0, "J5": 4, "J2": 9, "J3": 14, "J4": 19}
    assert all(cons.start[j] <= cons.reservation[j] for j in cons.start)


def random_jobs(rng, procs):
    jobs = []
    for i in range(rng.randrange(1, 9)):
        est = rng.randrange(1, 12)
        jobs.append(Job(f"j{i}", rng.randrange(0, 15), rng.randrange(1, procs + 1), est, rng.randrange(1, est + 4)))
    return jobs


def check_capacity(procs, jobs, tr):
    by = {j.name: j for j in jobs}
    assert set(tr.start) == set(tr.end) == set(by)
    for j in jobs:
        assert tr.start[j.name] >= j.arrival
        assert tr.end[j.name] - tr.start[j.name] == min(j.runtime, j.estimate)
    for t in {tr.start[n] for n in by}:
        assert sum(by[n].size for n in by if tr.start[n] <= t < tr.end[n]) <= procs


def shadow_at(t0, head, jobs, tr, procs):
    """Recompute, from the trace alone, the earliest time by the estimates of
    the jobs running at t0 at which the head would have enough processors."""
    run = [j for j in jobs if j.name != head.name and tr.start[j.name] <= t0 < tr.end[j.name]]
    busy = [(tr.start[j.name], tr.start[j.name] + j.estimate, j.size) for j in run]
    return earliest_fit(t0, head.size, 1, busy, procs)


def test_easy_never_delays_the_head() -> None:
    rng = random.Random(10)
    for _ in range(400):
        procs = rng.randrange(1, 7)
        jobs = random_jobs(rng, procs)
        tr = backfill(procs, jobs, "easy")
        check_capacity(procs, jobs, tr)
        order = sorted(jobs, key=lambda j: (j.arrival, j.name))
        for i, j in enumerate(order):
            # j is the head once it has arrived and all earlier jobs have started
            t0 = max([j.arrival] + [tr.start[k.name] for k in order[:i]])
            assert tr.start[j.name] <= shadow_at(t0, j, jobs, tr, procs)


def test_conservative_never_delays_a_reservation() -> None:
    rng = random.Random(11)
    for _ in range(400):
        procs = rng.randrange(1, 7)
        jobs = random_jobs(rng, procs)
        tr = backfill(procs, jobs, "conservative")
        check_capacity(procs, jobs, tr)
        for j in jobs:
            assert tr.start[j.name] <= tr.reservation[j.name]


def test_fcfs_keeps_order_and_backfilling_breaks_it() -> None:
    rng = random.Random(12)
    for _ in range(200):
        procs = rng.randrange(1, 7)
        jobs = random_jobs(rng, procs)
        tr = backfill(procs, jobs, "fcfs")
        check_capacity(procs, jobs, tr)
        order = sorted(jobs, key=lambda j: (j.arrival, j.name))
        starts = [tr.start[j.name] for j in order]
        assert starts == sorted(starts)
    easy = backfill(4, EXAMPLE, "easy")
    assert easy.start["J4"] < easy.start["J2"]


def test_edges() -> None:
    assert backfill(2, []).start == {}
    with pytest.raises(ValueError):
        backfill(2, [Job("X", 0, 3, 1, 1)])
    with pytest.raises(ValueError):
        backfill(2, [], "sjf")
    tr = backfill(2, [Job("X", 0, 1, 2, 9)], "easy")
    assert tr.end["X"] == 2  # killed at its estimate
