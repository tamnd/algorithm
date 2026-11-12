# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnsons-rule/. The authors are listed in prov/7Y0GYX.jsonl.

import itertools
import random

from johnsons_rule import gantt, johnsons_rule, makespan


def brute_force(a, b):
    return min(makespan(a, b, o) for o in itertools.permutations(range(len(a))))


def path_formula(a, b, order):
    """max over k of a(first k jobs) + b(jobs k to n), the longest path through the schedule."""
    if not order:
        return 0
    best = 0
    for k in range(len(order)):
        best = max(best, sum(a[j] for j in order[: k + 1]) + sum(b[j] for j in order[k:]))
    return best


def test_example() -> None:
    a = [4, 2, 6, 3, 5, 1]
    b = [3, 5, 2, 6, 5, 2]
    order = johnsons_rule(a, b)
    assert order == [5, 1, 3, 4, 0, 2]
    assert makespan(a, b, order) == 24
    assert brute_force(a, b) == 24
    assert makespan(a, b, range(6)) == 28
    assert gantt(a, b, order) == [
        (5, 0, 1, 1, 3),
        (1, 1, 3, 3, 8),
        (3, 3, 6, 8, 14),
        (4, 6, 11, 14, 19),
        (0, 11, 15, 19, 22),
        (2, 15, 21, 22, 24),
    ]
    # the bound min(a) + sum(b) is met, so the order is optimal by this bound alone
    assert min(a) + sum(b) == 24


def test_edges() -> None:
    assert johnsons_rule([], []) == []
    assert makespan([], [], []) == 0
    assert johnsons_rule([5], [1]) == [0]
    assert makespan([5], [1], [0]) == 6
    # a[j] == b[j] goes to the first group
    assert johnsons_rule([3, 3], [3, 1]) == [0, 1]
    # zero times
    assert makespan([0, 0], [4, 4], johnsons_rule([0, 0], [4, 4])) == 8


def test_against_all_orders() -> None:
    rng = random.Random(1954)
    for _ in range(300):
        n = rng.randrange(1, 8)
        a = [rng.randrange(0, 10) for _ in range(n)]
        b = [rng.randrange(0, 10) for _ in range(n)]
        order = johnsons_rule(a, b)
        assert sorted(order) == list(range(n))
        assert makespan(a, b, order) == brute_force(a, b)


def test_path_formula() -> None:
    rng = random.Random(2)
    for _ in range(200):
        n = rng.randrange(0, 9)
        a = [rng.randrange(0, 10) for _ in range(n)]
        b = [rng.randrange(0, 10) for _ in range(n)]
        order = list(range(n))
        rng.shuffle(order)
        assert makespan(a, b, order) == path_formula(a, b, order)


def test_lower_bounds_hold() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = rng.randrange(1, 12)
        a = [rng.randrange(1, 10) for _ in range(n)]
        b = [rng.randrange(1, 10) for _ in range(n)]
        c = makespan(a, b, johnsons_rule(a, b))
        assert c >= sum(a) + min(b)
        assert c >= min(a) + sum(b)
        assert c >= max(x + y for x, y in zip(a, b))
