# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-queue-scheduling/. The authors are listed in prov/KWDCKZ.jsonl.

import random

import pytest

from multilevel_queue_scheduling import Job, QueueSpec, multilevel_queue

EXAMPLE = [Job("A", 0, 3, 0), Job("B", 0, 4, 1), Job("C", 1, 2, 0), Job("D", 2, 3, 1), Job("E", 7, 2, 0)]
TWO = [QueueSpec("rr", 2), QueueSpec("fcfs")]


def show(tl):
    return "".join(x or "." for x in tl)


def test_example_fixed_priority() -> None:
    tl, done = multilevel_queue(EXAMPLE, TWO)
    assert show(tl) == "AACCABBEEBBDDD"
    assert done == {"C": 4, "A": 5, "E": 9, "B": 11, "D": 14}


def test_example_time_slicing() -> None:
    tl, done = multilevel_queue(EXAMPLE, TWO, "slice", [2, 1])
    assert show(tl) == "AABCCBAEBEBDDD"
    assert done == {"C": 5, "A": 7, "E": 10, "B": 11, "D": 14}


def test_edges() -> None:
    assert multilevel_queue([], TWO) == ([], {})
    tl, done = multilevel_queue([Job("X", 3, 2, 1)], TWO)
    assert show(tl) == "...XX" and done == {"X": 5}
    with pytest.raises(ValueError):
        multilevel_queue([Job("X", 0, 1, 2)], TWO)
    with pytest.raises(ValueError):
        multilevel_queue(EXAMPLE, TWO, "slice", [1])


def random_jobs(rng: random.Random, k: int) -> list[Job]:
    n = rng.randrange(1, 8)
    return [Job(f"j{i}", rng.randrange(10), rng.randrange(1, 6), rng.randrange(k)) for i in range(n)]


def test_fcfs_queues_against_reference() -> None:
    # With FCFS in every queue and fixed priority between queues, the job that
    # runs at each tick is the ready job with the smallest (class, arrival, index).
    rng = random.Random(7)
    for _ in range(600):
        k = rng.randrange(1, 4)
        jobs = random_jobs(rng, k)
        tl, done = multilevel_queue(jobs, [QueueSpec("fcfs")] * k)
        rem = {j.name: j.burst for j in jobs}
        want, t, fin = [], 0, {}
        while len(fin) < len(jobs):
            ready = [(j.cls, j.arrival, i) for i, j in enumerate(jobs) if j.arrival <= t and rem[j.name] > 0]
            if not ready:
                want.append(None)
            else:
                name = jobs[min(ready)[2]].name
                want.append(name)
                rem[name] -= 1
                if rem[name] == 0:
                    fin[name] = t + 1
            t += 1
        assert tl == want and done == fin


def test_jobs_never_move_and_higher_queues_are_isolated() -> None:
    rng = random.Random(11)
    for _ in range(500):
        k = rng.randrange(1, 4)
        queues = [QueueSpec(rng.choice(["rr", "fcfs"]), rng.randrange(1, 4)) for _ in range(k)]
        jobs = random_jobs(rng, k)
        cls = {j.name: j.cls for j in jobs}
        tl, done = multilevel_queue(jobs, queues)
        # a job runs only when no job of a higher queue is ready
        for t, name in enumerate(tl):
            if name is None:
                continue
            for j in jobs:
                if j.cls < cls[name] and j.arrival <= t < done[j.name]:
                    raise AssertionError("a lower queue ran while a higher one was ready")
        # the jobs of queues 0..c have the same schedule as without the lower queues
        for c in range(k):
            top = [j for j in jobs if j.cls <= c]
            _, d2 = multilevel_queue(top, queues)
            assert all(done[j.name] == d2[j.name] for j in top)


def test_time_slicing_gives_the_shares() -> None:
    # Three always-busy queues with shares 3, 2, 1: each cycle of 6 ticks
    # gives exactly 3, 2 and 1 ticks.
    jobs = [Job(f"q{c}j{i}", 0, 40, c) for c in range(3) for i in range(2)]
    queues = [QueueSpec("rr", 1), QueueSpec("rr", 2), QueueSpec("fcfs")]
    tl, _ = multilevel_queue(jobs, queues, "slice", [3, 2, 1])
    for start in range(0, 60, 6):
        part = tl[start : start + 6]
        counts = [sum(1 for x in part if x and x.startswith(f"q{c}")) for c in range(3)]
        assert counts == [3, 2, 1]


def test_work_conserving() -> None:
    rng = random.Random(3)
    for _ in range(300):
        k = rng.randrange(1, 4)
        jobs = random_jobs(rng, k)
        between = rng.choice(["priority", "slice"])
        shares = [rng.randrange(1, 4) for _ in range(k)]
        tl, done = multilevel_queue(jobs, [QueueSpec("rr", 2)] * k, between, shares)
        for t, name in enumerate(tl):
            ready = any(j.arrival <= t < done[j.name] for j in jobs)
            assert (name is not None) == ready
        assert sum(1 for x in tl if x) == sum(j.burst for j in jobs)
