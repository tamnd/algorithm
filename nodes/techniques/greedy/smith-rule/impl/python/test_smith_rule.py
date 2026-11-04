# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-rule/. The authors are listed in prov/5N4EPA.jsonl.

import itertools
import math
import random

import pytest

from smith_rule import smith_rule


def cost(jobs, order):
    t = total = 0
    for j in order:
        t += jobs[j][0]
        total += jobs[j][1] * t
    return total


def test_example() -> None:
    names = "ABCDEF"
    jobs = [(3, 1), (1, 2), (4, 4), (2, 5), (5, 3), (2, 2)]
    order, total = smith_rule(jobs)
    assert "".join(names[j] for j in order) == "DBCFEA"
    assert total == 121
    assert min(cost(jobs, p) for p in itertools.permutations(range(6))) == 121


def test_edges() -> None:
    assert smith_rule([]) == ([], 0)
    assert smith_rule([(5, 7)]) == ([0], 35)
    assert smith_rule([(2, 2), (2, 2), (2, 2)]) == ([0, 1, 2], 2 * 2 + 2 * 4 + 2 * 6)
    order, total = smith_rule([(1, 0), (3, 1)])
    assert order == [1, 0] and total == 3
    with pytest.raises(ValueError):
        smith_rule([(0, 1)])


def test_pitfall_keys() -> None:
    jobs = [(3, 1), (1, 2), (4, 4), (2, 5), (5, 3), (2, 2)]
    spt = sorted(range(6), key=lambda j: jobs[j][0])
    heavy = sorted(range(6), key=lambda j: -jobs[j][1])
    assert cost(jobs, spt) == 134 and cost(jobs, heavy) == 136


def test_negative_weights() -> None:
    jobs = [(2, -3), (1, 4), (3, 0), (1, -1)]
    _, total = smith_rule(jobs)
    assert total == min(cost(jobs, p) for p in itertools.permutations(range(4)))


def test_against_brute_force() -> None:
    rng = random.Random(9031)
    for _ in range(600):
        n = rng.randrange(0, 7)
        jobs = [(rng.randrange(1, 8), rng.randrange(0, 8)) for _ in range(n)]
        order, total = smith_rule(jobs)
        assert sorted(order) == list(range(n))
        assert total == cost(jobs, order)
        assert total == min(cost(jobs, p) for p in itertools.permutations(range(n)))


def test_floats() -> None:
    jobs = [(0.5, 1.0), (1.5, 2.0), (0.25, 0.1)]
    order, total = smith_rule(jobs)
    best = min(cost(jobs, p) for p in itertools.permutations(range(3)))
    assert math.isclose(total, best, rel_tol=1e-12)


def test_large_integers() -> None:
    jobs = [(2**40 + 1, 2**41), (2**40, 2**41 - 1)]
    order, total = smith_rule(jobs)
    assert total == min(cost(jobs, p) for p in itertools.permutations(range(2)))
