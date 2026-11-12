# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yds-algorithm/. The authors are listed in prov/ZZVKP5.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from yds_algorithm import avr_energy, yds

EXAMPLE = [(0, 2, 4), (0, 8, 4), (4, 6, 3)]


def check_schedule(jobs, sched) -> None:
    """Each job gets exactly its work inside its window, and no two segments overlap."""
    done = [F(0)] * len(jobs)
    last = None
    for a, b, j in sched.segments:
        r, d, _ = jobs[j]
        assert r <= a < b <= d
        assert last is None or last <= a
        last = b
        done[j] += (b - a) * sched.speed[j]
    assert done == [F(w) for _, _, w in jobs]


def test_hand_example() -> None:
    s = yds(EXAMPLE)
    assert [(r.speed, r.pieces, r.jobs) for r in s.rounds] == [
        (2, [(0, 2)], [0]),
        (F(3, 2), [(4, 6)], [2]),
        (1, [(2, 4), (6, 8)], [1]),
    ]
    assert s.segments == [(0, 2, 0), (2, 4, 1), (4, 6, 2), (6, 8, 1)]
    assert s.energy(3) == F(107, 4)  # 4*4 + 3*(9/4) + 4*1
    assert avr_energy(EXAMPLE, 3) == F(191, 4)
    check_schedule(EXAMPLE, s)


def random_jobs(rng, n, horizon, max_work):
    out = []
    for _ in range(n):
        r = rng.randrange(0, horizon)
        d = rng.randrange(r + 1, horizon + 1)
        out.append((r, d, rng.randrange(1, max_work + 1)))
    return out


def intensity_max(jobs):
    pts = sorted({p for r, d, _ in jobs for p in (r, d)})
    return max(
        F(sum(w for r, d, w in jobs if a <= r and d <= b), b - a) for a in pts for b in pts if a < b
    )


def test_structure_on_random_instances() -> None:
    rng = random.Random(5)
    for _ in range(300):
        jobs = random_jobs(rng, rng.randrange(1, 8), 12, 6)
        s = yds(jobs)
        check_schedule(jobs, s)
        speeds = [r.speed for r in s.rounds]
        assert speeds == sorted(speeds, reverse=True)  # rounds never speed up
        assert speeds[0] == intensity_max(jobs)  # the first round is the densest interval
        for alpha in (2, 3):
            assert s.energy(alpha) == sum(F(w) * s.speed[j] ** (alpha - 1) for j, (_, _, w) in enumerate(jobs))
            assert s.energy(alpha) <= avr_energy(jobs, alpha)
        # every job of round k lies inside the time used by rounds 1..k
        covered = []
        for rd in s.rounds:
            covered += rd.pieces
            for j in rd.jobs:
                r, d, _ = jobs[j]
                inside = sum(max(F(0), min(b, d) - max(a, r)) for a, b in covered)
                assert inside == d - r


def feasible(jobs, slot_speed) -> bool:
    # Preemptive jobs with windows can run at these unit slot speeds iff no
    # interval holds more work than its capacity.
    T = len(slot_speed)
    for a in range(T):
        for b in range(a + 1, T + 1):
            if sum(w for r, d, w in jobs if a <= r and d <= b) > sum(slot_speed[a:b]):
                return False
    return True


def test_against_brute_force_over_discrete_speeds() -> None:
    rng = random.Random(6)
    grid = [F(k, 2) for k in range(9)]  # speeds 0, 1/2, ..., 4 in each unit slot
    checked = exact = 0
    while checked < 25:
        jobs = random_jobs(rng, rng.randrange(1, 4), 4, 3)
        s = yds(jobs)
        if max(s.speed.values()) > 4:
            continue
        checked += 1
        alpha = 3
        best = min(
            sum(v**alpha for v in prof) for prof in itertools.product(grid, repeat=4) if feasible(jobs, prof)
        )
        assert best >= s.energy(alpha)  # YDS is a lower bound for every schedule
        on_grid = all((v * 2).denominator == 1 for v in s.speed.values())
        if on_grid:
            exact += 1
            assert best == s.energy(alpha)
    assert exact >= 10


def test_single_job_and_edges() -> None:
    s = yds([(1, 5, 2)])
    assert s.speed == {0: F(1, 2)} and s.segments == [(1, 5, 0)]
    assert s.energy(2) == 1  # 4 time units at speed 1/2, power 1/4
    with pytest.raises(ValueError):
        yds([(3, 3, 1)])
    with pytest.raises(ValueError):
        yds([(0, 1, 0)])
    assert yds([]).segments == []
