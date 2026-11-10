# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-with-release-dates/. The authors are listed in prov/N7DJXC.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from scheduling_with_release_dates import erd_schedule, is_feasible, single_machine_lower_bound


def one_machine_value(p, r, order):
    t = 0
    for j in order:
        t = max(t, r[j]) + p[j]
    return t


def best_makespan(p, r, m):
    """Search over all assignments; each machine runs its jobs by release date, which is optimal for it."""
    n = len(p)
    best = None
    for assign in itertools.product(range(m), repeat=n):
        v = 0
        for i in range(m):
            jobs = sorted((j for j in range(n) if assign[j] == i), key=lambda j: r[j])
            v = max(v, one_machine_value(p, r, jobs))
        if best is None or v < best:
            best = v
    return best


def test_page_examples() -> None:
    p, r = [2, 3, 1, 2], [4, 0, 1, 9]
    machine, start, cmax = erd_schedule(p, r)
    assert start == [4, 0, 3, 9] and cmax == 11 == single_machine_lower_bound(p, r)
    # the tight family for m = 2: two unit jobs, then a job of length 2, all at time 0
    assert erd_schedule([1, 1, 2], [0, 0, 0], 2)[2] == 3 and best_makespan([1, 1, 2], [0, 0, 0], 2) == 2


def test_one_machine_is_optimal() -> None:
    rng = random.Random(71)
    for _ in range(300):
        n = rng.randint(0, 7)
        p = [rng.randint(0, 6) for _ in range(n)]
        r = [rng.randint(0, 15) for _ in range(n)]
        machine, start, cmax = erd_schedule(p, r)
        assert is_feasible(p, r, machine, start)
        brute = min((one_machine_value(p, r, o) for o in itertools.permutations(range(n))), default=0)
        assert cmax == brute == single_machine_lower_bound(p, r)


def test_parallel_machines_ratio() -> None:
    rng = random.Random(72)
    for _ in range(200):
        m = rng.randint(2, 3)
        n = rng.randint(1, 7)
        p = [rng.randint(1, 6) for _ in range(n)]
        r = [rng.randint(0, 10) for _ in range(n)]
        machine, start, cmax = erd_schedule(p, r, m)
        assert is_feasible(p, r, machine, start)
        opt = best_makespan(p, r, m)
        last = max(range(n), key=lambda j: start[j] + p[j])
        assert opt <= cmax <= 2 * opt - Fraction(p[last], m)  # the proven bound
        assert cmax <= Fraction(2 * m - 1, m) * opt  # observed on these instances


def test_tight_family() -> None:
    for m in range(2, 5):
        p = [1] * (m * (m - 1)) + [m]
        r = [0] * len(p)
        assert erd_schedule(p, r, m)[2] == 2 * m - 1
        # OPT = m: the long job alone on one machine, m unit jobs on each other machine
        assert single_machine_lower_bound([m], [0]) == m


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        erd_schedule([1], [0, 1])
    with pytest.raises(ValueError):
        erd_schedule([1], [-1])
    with pytest.raises(ValueError):
        erd_schedule([1], [0], 0)
