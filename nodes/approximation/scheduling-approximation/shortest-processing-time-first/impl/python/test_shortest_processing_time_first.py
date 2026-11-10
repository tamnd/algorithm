# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shortest-processing-time-first/. The authors are listed in prov/VXZQYC.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from shortest_processing_time_first import shortest_processing_time_first, total_completion_time


def best_one_machine(p):
    best = None
    for order in itertools.permutations(range(len(p))):
        v = total_completion_time(p, [list(order)])
        best = v if best is None or v < best else best
    return best if best is not None else 0


def brute_force(p, m):
    """Least total completion time over all assignments and all orders."""
    best = None
    for assign in itertools.product(range(m), repeat=len(p)):
        v = 0
        for i in range(m):
            v += best_one_machine([p[j] for j in range(len(p)) if assign[j] == i])
        best = v if best is None or v < best else best
    return best


def greedy_list(p, m):
    """SPT list scheduling: the next shortest job goes to the machine that is free first."""
    load = [0] * m
    total = 0
    for j in sorted(range(len(p)), key=lambda j: (p[j], j)):
        i = min(range(m), key=lambda i: (load[i], i))
        load[i] += p[j]
        total += load[i]
    return total


def test_example() -> None:
    p = [4, 1, 3, 6, 2]
    machines, completion, total = shortest_processing_time_first(p)
    assert machines == [[1, 4, 2, 0, 3]]
    assert completion == [10, 1, 6, 16, 3]
    assert total == 36
    machines, completion, total = shortest_processing_time_first(p, 2)
    assert machines == [[1, 2, 3], [4, 0]]
    assert total == 1 + 4 + 10 + 2 + 6
    assert total_completion_time(p, [[3, 0, 2, 4, 1]]) == 6 + 10 + 13 + 15 + 16


def test_edges() -> None:
    assert shortest_processing_time_first([]) == ([[]], [], 0)
    assert shortest_processing_time_first([5], 3)[2] == 5
    assert shortest_processing_time_first([0, 0, 2])[2] == 2
    assert shortest_processing_time_first([Fraction(1, 2), Fraction(1, 3)])[2] == Fraction(7, 6)
    with pytest.raises(ValueError):
        shortest_processing_time_first([1], 0)
    with pytest.raises(ValueError):
        shortest_processing_time_first([-1])


def test_one_machine_against_all_orders() -> None:
    rng = random.Random(11)
    for _ in range(200):
        p = [rng.randint(0, 9) for _ in range(rng.randint(0, 7))]
        assert shortest_processing_time_first(p)[2] == best_one_machine(p)


def test_parallel_against_brute_force() -> None:
    rng = random.Random(12)
    for _ in range(60):
        m = rng.randint(2, 3)
        p = [rng.randint(1, 9) for _ in range(rng.randint(1, 6))]
        machines, completion, total = shortest_processing_time_first(p, m)
        assert sorted(j for js in machines for j in js) == list(range(len(p)))
        assert total == total_completion_time(p, machines) == sum(completion)
        assert total == brute_force(p, m)
        assert greedy_list(p, m) == total


def test_positional_formula() -> None:
    rng = random.Random(13)
    for _ in range(200):
        m = rng.randint(1, 4)
        n = rng.randint(0, 12)
        p = [rng.randint(0, 20) for _ in range(n)]
        q = sorted(p, reverse=True)
        want = sum(-(-k // m) * q[k - 1] for k in range(1, n + 1))
        assert shortest_processing_time_first(p, m)[2] == want
