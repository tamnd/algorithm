# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jonker-volgenant-algorithm/. The authors are listed in prov/TN0EFM.jsonl.

import itertools
import random

from jonker_volgenant_algorithm import jonker_volgenant_algorithm


def check(cost, passes=2):
    """The result is a permutation with a feasible dual of equal value. Returns its cost."""
    n = len(cost)
    x, u, v = jonker_volgenant_algorithm(cost, passes)
    assert sorted(x) == list(range(n))
    for i in range(n):
        for j in range(n):
            assert u[i] + v[j] <= cost[i][j]
        assert u[i] + v[x[i]] == cost[i][x[i]]
    total = sum(cost[i][x[i]] for i in range(n))
    assert total == sum(u) + sum(v)
    return total


def brute(cost):
    n = len(cost)
    return min((sum(cost[i][p[i]] for i in range(n)) for p in itertools.permutations(range(n))), default=0)


def test_empty_and_one():
    assert jonker_volgenant_algorithm([]) == ([], [], [])
    assert check([[7]]) == 7
    assert check([[-3]]) == -3


def test_worked_example():
    cost = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
    assert check(cost) == 5
    assert jonker_volgenant_algorithm(cost)[0] == [1, 0, 2]


def test_all_equal_and_ties():
    assert check([[5] * 4 for _ in range(4)]) == 20
    assert check([[0, 0], [0, 0]]) == 0


def test_forbidden_pairs_by_large_cost():
    # a large cost stands for a missing edge; this graph has no perfect matching
    # of finite pairs, so the optimum must use one large pair
    big = 10**6
    cost = [[1, big, big], [2, big, big], [big, 3, 4]]
    assert check(cost) == brute(cost) == 1 + big + 3


def test_not_square():
    try:
        jonker_volgenant_algorithm([[1, 2]])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_random_against_brute_force():
    rng = random.Random(1987)
    for _ in range(1500):
        n = rng.randint(0, 6)
        hi = rng.choice([1, 3, 10, 1000])
        cost = [[rng.randint(-hi, hi) for _ in range(n)] for _ in range(n)]
        best = brute(cost)
        for passes in (0, 1, 2):
            assert check(cost, passes) == best


def test_larger_random_dual_certificate():
    rng = random.Random(5)
    for _ in range(20):
        n = rng.randint(20, 60)
        cost = [[rng.randint(0, 50) for _ in range(n)] for _ in range(n)]
        check(cost)
        check(cost, 0)
