# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-scheduling/. The authors are listed in prov/D4MGPF.jsonl.

import itertools
import random
from fractions import Fraction

from list_scheduling import list_scheduling, list_scheduling_with_precedence


def brute_opt(p: list[int], m: int) -> int:
    """Optimal makespan by trying every assignment (job 0 fixed to machine 0)."""
    if not p:
        return 0
    best = None
    for rest in itertools.product(range(m), repeat=len(p) - 1):
        load = [0] * m
        for x, i in zip(p, (0,) + rest):
            load[i] += x
        if best is None or max(load) < best:
            best = max(load)
    return best


def check_schedule(p, m, machine, start, makespan) -> None:
    by_machine = {}
    for j, (i, s) in enumerate(zip(machine, start)):
        assert 0 <= i < m and s >= 0
        by_machine.setdefault(i, []).append((s, s + p[j]))
    for runs in by_machine.values():
        runs.sort()
        for (a, b), (c, d) in zip(runs, runs[1:]):
            assert b <= c
    assert makespan == max((s + x for s, x in zip(start, p)), default=0)


def test_example() -> None:
    p = [2, 3, 4, 6, 2, 2]
    machine, start, makespan = list_scheduling(p, 3)
    assert machine == [0, 1, 2, 0, 1, 2]
    assert start == [0, 0, 0, 2, 3, 4]
    assert makespan == 8
    assert brute_opt(p, 3) == 7


def test_edges() -> None:
    assert list_scheduling([], 3) == ([], [], 0)
    assert list_scheduling([5], 1) == ([0], [0], 5)
    assert list_scheduling([4, 1, 2], 1)[2] == 7
    assert list_scheduling([3, 3], 5)[2] == 3
    assert list_scheduling([2, 2, 2, 2], 2)[2] == 4


def test_against_brute_force() -> None:
    rng = random.Random(11)
    for _ in range(600):
        m = rng.randrange(1, 4)
        p = [rng.randrange(0, 10) for _ in range(rng.randrange(0, 8))]
        machine, start, makespan = list_scheduling(p, m)
        check_schedule(p, m, machine, start, makespan)
        opt = brute_opt(p, m)
        assert Fraction(sum(p), m) <= opt and max(p, default=0) <= opt
        assert makespan <= (2 - Fraction(1, m)) * opt
        # the bound of the proof: average load plus (1 - 1/m) times the last job
        last = max(range(len(p)), key=lambda j: start[j] + p[j], default=None)
        if last is not None:
            assert makespan <= Fraction(sum(p), m) + (1 - Fraction(1, m)) * p[last]


def test_online_prefix() -> None:
    rng = random.Random(12)
    for _ in range(200):
        m = rng.randrange(1, 5)
        p = [rng.randrange(1, 9) for _ in range(rng.randrange(1, 12))]
        full = list_scheduling(p, m)
        for k in range(len(p) + 1):
            part = list_scheduling(p[:k], m)
            assert part[0] == full[0][:k] and part[1] == full[1][:k]


def test_tight_family() -> None:
    for m in range(1, 8):
        p = [1] * (m * (m - 1)) + [m]
        assert list_scheduling(p, m)[2] == 2 * m - 1
        assert list_scheduling(sorted(p, reverse=True), m)[2] == m


def test_precedence_matches_plain_without_constraints() -> None:
    rng = random.Random(13)
    for _ in range(300):
        m = rng.randrange(1, 4)
        p = [rng.randrange(1, 9) for _ in range(rng.randrange(1, 8))]
        a = list_scheduling(p, m)[2]
        b = list_scheduling_with_precedence(p, m, [], list(range(len(p))))[2]
        assert a == b


def test_graham_anomalies() -> None:
    p = [3, 2, 2, 2, 4, 4, 4, 4, 9]
    prec = [(0, 8), (3, 4), (3, 5), (3, 6), (3, 7)]
    order = list(range(9))
    assert list_scheduling_with_precedence(p, 3, prec, order)[2] == 12
    assert list_scheduling_with_precedence(p, 3, prec, [0, 1, 3, 4, 5, 2, 8, 6, 7])[2] == 14
    assert list_scheduling_with_precedence(p, 4, prec, order)[2] == 15
    assert list_scheduling_with_precedence([x - 1 for x in p], 3, prec, order)[2] == 13
    assert list_scheduling_with_precedence(p, 3, [(0, 8), (3, 6), (3, 7)], order)[2] == 16
