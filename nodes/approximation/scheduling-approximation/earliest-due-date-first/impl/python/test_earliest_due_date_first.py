# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/earliest-due-date-first/. The authors are listed in prov/9Q08CA.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from earliest_due_date_first import earliest_due_date_first, max_lateness


def brute_force(p, d):
    return min(max_lateness(p, d, o) for o in itertools.permutations(range(len(p))))


def test_example() -> None:
    p = [3, 2, 1, 4, 2]
    d = [5, 4, 9, 10, 3]
    order, completion, lmax = earliest_due_date_first(p, d)
    assert order == [4, 1, 0, 2, 3]
    assert completion == [7, 4, 8, 12, 2]
    assert lmax == 2 == brute_force(p, d)
    assert max_lateness(p, d, sorted(range(5), key=lambda j: (p[j], j))) == 3
    assert max_lateness(p, d, sorted(range(5), key=lambda j: (d[j] - p[j], j))) == 3


def test_min_slack_counterexample() -> None:
    p, d = [5, 2], [6, 4]
    assert max_lateness(p, d, [0, 1]) == 3
    assert earliest_due_date_first(p, d)[2] == 1


def test_edges() -> None:
    assert earliest_due_date_first([], []) == ([], [], None)
    assert earliest_due_date_first([3], [1])[2] == 2
    assert earliest_due_date_first([1, 1], [-5, -5])[2] == 7
    assert earliest_due_date_first([Fraction(1, 2), 1], [1, Fraction(1, 3)])[2] == Fraction(2, 3)
    with pytest.raises(ValueError):
        earliest_due_date_first([1], [])
    with pytest.raises(ValueError):
        earliest_due_date_first([-1], [0])


def test_against_all_orders() -> None:
    rng = random.Random(21)
    for _ in range(300):
        n = rng.randint(1, 7)
        p = [rng.randint(0, 8) for _ in range(n)]
        d = [rng.randint(-5, 25) for _ in range(n)]
        order, completion, lmax = earliest_due_date_first(p, d)
        assert sorted(order) == list(range(n))
        assert lmax == max(completion[j] - d[j] for j in range(n))
        assert lmax == brute_force(p, d)


def test_lower_bound_witness() -> None:
    # The job that attains Lmax in EDD and the jobs before it form a set A whose
    # last job, in any order, is at least as late: p(A) - max d over A = Lmax.
    rng = random.Random(22)
    for _ in range(300):
        n = rng.randint(1, 8)
        p = [rng.randint(1, 8) for _ in range(n)]
        d = [rng.randint(0, 30) for _ in range(n)]
        order, completion, lmax = earliest_due_date_first(p, d)
        k = max(range(n), key=lambda i: completion[order[i]] - d[order[i]])
        a = order[: k + 1]
        assert sum(p[j] for j in a) - max(d[j] for j in a) == lmax


def test_feasibility_test_for_deadlines() -> None:
    rng = random.Random(23)
    for _ in range(200):
        n = rng.randint(1, 6)
        p = [rng.randint(1, 5) for _ in range(n)]
        d = [rng.randint(1, 20) for _ in range(n)]
        some = any(max_lateness(p, d, o) <= 0 for o in itertools.permutations(range(n)))
        assert some == (earliest_due_date_first(p, d)[2] <= 0)
