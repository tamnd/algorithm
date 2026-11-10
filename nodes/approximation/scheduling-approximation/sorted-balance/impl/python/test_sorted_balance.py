# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sorted-balance/. The authors are listed in prov/SYMRSF.jsonl.

import itertools
import random
from fractions import Fraction

from sorted_balance import sorted_balance


def brute_opt(p: list[int], m: int) -> int:
    if not p:
        return 0
    best = None
    for rest in itertools.product(range(m), repeat=len(p) - 1):
        load = [0] * m
        for x, i in zip(p, (0,) + rest):
            load[i] += x
        best = max(load) if best is None else min(best, max(load))
    return best


def test_example() -> None:
    p = [6, 5, 4, 4, 3, 3, 2]
    a, t = sorted_balance(p, 3)
    assert a == [[0, 5], [1, 4, 6], [2, 3]]
    assert t == [9, 10, 8]
    assert brute_opt(p, 3) == 9


def test_edges() -> None:
    assert sorted_balance([], 2) == ([[], []], [0, 0])
    assert sorted_balance([7], 3) == ([[0], [], []], [7, 0, 0])
    assert sorted_balance([1, 2, 3], 1) == ([[2, 1, 0]], [6])
    assert sorted_balance([2, 2, 2], 3)[1] == [2, 2, 2]


def test_is_a_partition() -> None:
    rng = random.Random(31)
    for _ in range(300):
        m = rng.randrange(1, 5)
        p = [rng.randrange(0, 15) for _ in range(rng.randrange(0, 12))]
        a, t = sorted_balance(p, m)
        assert sorted(j for jobs in a for j in jobs) == list(range(len(p)))
        assert [sum(p[j] for j in jobs) for jobs in a] == t


def test_against_brute_force() -> None:
    rng = random.Random(32)
    for _ in range(600):
        m = rng.randrange(1, 4)
        n = rng.randrange(0, 8)
        p = [rng.randrange(1, 13) for _ in range(n)]
        opt = brute_opt(p, m)
        alg = max(sorted_balance(p, m)[1], default=0)
        s = sorted(p, reverse=True)
        if n > m:
            assert 2 * s[m] <= opt and s[m - 1] + s[m] <= opt
        else:
            assert alg == opt
        assert Fraction(sum(p), m) <= opt
        assert alg <= (Fraction(3, 2) - Fraction(1, 2 * m)) * opt


def test_bound_not_reached_for_two_machines() -> None:
    # the true worst case on two machines is 7/6 < 5/4
    p = [3, 3, 2, 2, 2]
    assert max(sorted_balance(p, 2)[1]) == 7 and brute_opt(p, 2) == 6
