# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-metrics/. The authors are listed in prov/NMZMS9.jsonl.

import random
from fractions import Fraction

import pytest

from scheduling_metrics import aggregate, jain_index, number_in_system_area, per_job

JOBS = [("P1", 0, 8), ("P2", 1, 4), ("P3", 2, 9), ("P4", 3, 5)]
RR4 = [(0, 4, "P1"), (4, 8, "P2"), (8, 12, "P3"), (12, 16, "P4"),
       (16, 20, "P1"), (20, 24, "P3"), (24, 25, "P4"), (25, 26, "P3")]
FCFS = [(0, 8, "P1"), (8, 12, "P2"), (12, 21, "P3"), (21, 26, "P4")]


def test_round_robin_table() -> None:
    m = per_job(JOBS, RR4)
    assert [(m[p].completion, m[p].turnaround, m[p].waiting, m[p].response) for p in ("P1", "P2", "P3", "P4")] == [
        (20, 20, 12, 0), (8, 7, 3, 3), (26, 24, 15, 6), (25, 22, 17, 9)]
    assert [m[p].stretch for p in ("P1", "P2", "P3", "P4")] == [
        Fraction(5, 2), Fraction(7, 4), Fraction(8, 3), Fraction(22, 5)]
    a = aggregate(JOBS, RR4)
    assert a["avg_turnaround"] == Fraction(73, 4)
    assert a["avg_waiting"] == Fraction(47, 4)
    assert a["avg_response"] == Fraction(9, 2)
    assert a["max_stretch"] == Fraction(22, 5)
    assert a["throughput"] == Fraction(2, 13)
    assert a["utilization"] == 1


def test_fcfs_table() -> None:
    m = per_job(JOBS, FCFS)
    assert [m[p].turnaround for p in ("P1", "P2", "P3", "P4")] == [8, 11, 19, 23]
    assert all(m[p].waiting == m[p].response for p in m)  # nonpreemptive
    a = aggregate(JOBS, FCFS)
    assert a["avg_turnaround"] == Fraction(61, 4)
    assert a["avg_waiting"] == a["avg_response"] == Fraction(35, 4)
    assert a["max_stretch"] == Fraction(23, 5)


def test_little_identity_on_example() -> None:
    for segs in (RR4, FCFS):
        area = number_in_system_area(JOBS, segs)
        a = aggregate(JOBS, segs)
        assert area == sum(m.turnaround for m in per_job(JOBS, segs).values())
        assert Fraction(area, 26) == a["throughput"] * a["avg_turnaround"]


def test_jain() -> None:
    assert jain_index([3, 3, 3]) == 1
    assert jain_index([1, 0, 0, 0]) == Fraction(1, 4)
    assert jain_index([8, 4, 4, 0]) == Fraction(2, 3)


def test_bad_schedules() -> None:
    with pytest.raises(ValueError):
        per_job(JOBS, RR4[:-1])
    with pytest.raises(ValueError):
        per_job([("A", 2, 1)], [(1, 2, "A")])


def test_identities_random() -> None:
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randrange(1, 6)
        jobs = [(f"j{i}", rng.randrange(10), rng.randrange(1, 6)) for i in range(n)]
        t, segs = 0, []
        for name, a, b in sorted(jobs, key=lambda j: j[1]):
            t = max(t, a)
            segs.append((t, t + b, name))
            t += b
        m = per_job(jobs, segs)
        for name, a, b in jobs:
            x = m[name]
            assert x.waiting == x.response >= 0  # one piece per job
            assert x.turnaround == x.waiting + b
            assert x.stretch >= 1
