# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sjf-optimality/. The authors are listed in prov/137WN4.jsonl.

import itertools
import random
from fractions import Fraction

from sjf_optimality import (best_nonpreemptive, formula, preemptive_waiting, sjf_order,
                            srpt_slices, total_waiting)


def test_examples() -> None:
    b = [6, 8, 7, 3]
    assert total_waiting(sjf_order(b), b) == 28  # mean 7
    assert total_waiting([0, 1, 2, 3], b) == 41  # FCFS, mean 10.25
    assert formula(b) == 28
    assert total_waiting(sjf_order([24, 3, 3]), [24, 3, 3]) == 9


def test_sjf_is_optimal_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(400):
        n = rng.randrange(1, 8)
        b = [rng.randrange(1, 12) for _ in range(n)]
        best = min(total_waiting(list(p), b) for p in itertools.permutations(range(n)))
        assert total_waiting(sjf_order(b), b) == best == formula(b)


def test_only_sorted_orders_are_optimal() -> None:
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randrange(2, 7)
        b = [rng.randrange(1, 6) for _ in range(n)]
        best = formula(b)
        for p in itertools.permutations(range(n)):
            sorted_ = all(b[p[k]] <= b[p[k + 1]] for k in range(n - 1))
            assert (total_waiting(list(p), b) == best) == sorted_


def test_adjacent_swap_gain() -> None:
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randrange(2, 8)
        b = [rng.randrange(1, 20) for _ in range(n)]
        p = list(range(n))
        rng.shuffle(p)
        k = rng.randrange(n - 1)
        q = p[:]
        q[k], q[k + 1] = q[k + 1], q[k]
        # moving the later job ahead changes the total by (its burst) - (the other burst)
        assert total_waiting(q, b) - total_waiting(p, b) == b[p[k + 1]] - b[p[k]]


def test_preemption_does_not_help_at_time_zero() -> None:
    rng = random.Random(4)
    for _ in range(400):
        n = rng.randrange(1, 5)
        b = [rng.randrange(1, 4) for _ in range(n)]
        slots = [j for j in range(n) for _ in range(b[j])]
        rng.shuffle(slots)  # a random preemptive schedule with no idle time
        if rng.random() < 0.3:
            slots.insert(rng.randrange(len(slots) + 1), None)
        assert preemptive_waiting([0] * n, b, slots) >= formula(b)


def test_fails_with_arrivals() -> None:
    a, b = [0, 1], [10, 1]
    sjf_nonpreemptive = 0 + 9  # the CPU is free at 0 and only the long burst has arrived
    assert best_nonpreemptive(a, b) == 2  # idle on [0, 1), short, then long
    assert sjf_nonpreemptive > best_nonpreemptive(a, b)
    assert preemptive_waiting(a, b, srpt_slices(a, b)) == 1


def test_fraction_bursts() -> None:
    b = [Fraction(5, 2), Fraction(1, 3), Fraction(7, 4)]
    best = min(total_waiting(list(p), b) for p in itertools.permutations(range(3)))
    assert total_waiting(sjf_order(b), b) == best == formula(b)
