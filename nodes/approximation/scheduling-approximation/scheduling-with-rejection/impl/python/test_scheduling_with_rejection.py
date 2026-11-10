# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scheduling-with-rejection/. The authors are listed in prov/NKR10R.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from scheduling_with_rejection import cost, list_schedule, threshold_rejection


def brute_force(p, e, m):
    """Each job is rejected (-1) or put on one of the m machines."""
    n = len(p)
    best = None
    for choice in itertools.product(range(-1, m), repeat=n):
        loads = [0] * m
        pen = 0
        for j, c in enumerate(choice):
            if c < 0:
                pen += e[j]
            else:
                loads[c] += p[j]
        v = max(loads) + pen
        if best is None or v < best:
            best = v
    return best


def check(p, e, m, machines, rejected, value):
    assert sorted([j for mach in machines for j in mach] + list(rejected)) == list(range(len(p)))
    assert cost(p, e, machines, rejected) == value


def test_page_example() -> None:
    p, e = [6, 4, 3, 3, 2, 2], [2, 5, 4, 1, 3, 1]
    machines, rejected, value = threshold_rejection(p, e, 2)
    check(p, e, 2, machines, rejected, value)
    assert machines == [[1, 5], [2, 4]] and rejected == [0, 3] and value == 9
    assert brute_force(p, e, 2) == 9
    # a job is rejected although a machine is idle
    machines, rejected, value = threshold_rejection([4, 4], [1, 4], 2)
    assert value == 5 and brute_force([4, 4], [1, 4], 2) == 4


def test_tight_family() -> None:
    # m jobs of length mK; job 0 has a huge penalty, the others K - 1
    K = 5
    for m in range(2, 5):
        p = [m * K] * m
        e = [10**6] + [K - 1] * (m - 1)
        assert threshold_rejection(p, e, m)[2] == m * K + (m - 1) * (K - 1)
        assert brute_force(p, e, m) == m * K


def test_one_machine_is_optimal() -> None:
    rng = random.Random(101)
    for _ in range(200):
        n = rng.randint(0, 7)
        p = [rng.randint(0, 8) for _ in range(n)]
        e = [rng.randint(0, 8) for _ in range(n)]
        machines, rejected, value = threshold_rejection(p, e, 1)
        check(p, e, 1, machines, rejected, value)
        assert value == brute_force(p, e, 1)


def test_ratio_on_parallel_machines() -> None:
    rng = random.Random(102)
    for _ in range(200):
        m = rng.randint(2, 3)
        n = rng.randint(1, 6)
        p = [rng.randint(1, 9) for _ in range(n)]
        e = [rng.randint(0, 9) for _ in range(n)]
        machines, rejected, value = threshold_rejection(p, e, m)
        check(p, e, m, machines, rejected, value)
        opt = brute_force(p, e, m)
        assert opt <= value <= Fraction(2 * m - 1, m) * opt


def test_large_penalties_give_plain_makespan() -> None:
    p = [3, 3, 2, 2, 2]
    machines, rejected, value = threshold_rejection(p, [100] * 5, 2)
    assert rejected == [] and value == list_schedule(p, range(5), 2)[1] == 7


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        threshold_rejection([1], [1, 2], 1)
    with pytest.raises(ValueError):
        threshold_rejection([1], [-1], 1)
    with pytest.raises(ValueError):
        threshold_rejection([1], [1], 0)
