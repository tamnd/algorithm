# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smiths-rule/. The authors are listed in prov/51P9W7.jsonl.

import itertools
import random
from fractions import Fraction

from smiths_rule import smiths_rule, weighted_completion_time


def brute_force(p, w):
    return min(weighted_completion_time(p, w, o) for o in itertools.permutations(range(len(p))))


def test_example() -> None:
    p = [8, 2, 5, 3, 6]
    w = [4, 1, 5, 1, 2]
    order = smiths_rule(p, w)
    assert order == [2, 0, 1, 3, 4]
    assert weighted_completion_time(p, w, order) == 158
    assert brute_force(p, w) == 158
    # shortest first and heaviest first both lose
    assert weighted_completion_time(p, w, [1, 3, 2, 4, 0]) == 185
    assert weighted_completion_time(p, w, [2, 0, 4, 1, 3]) == 160


def test_edges() -> None:
    assert smiths_rule([], []) == []
    assert smiths_rule([7], [3]) == [0]
    # equal ratios keep the input order
    assert smiths_rule([2, 4, 1], [1, 2, 1]) == [2, 0, 1]
    # weight 0 goes last, processing time 0 goes first
    assert smiths_rule([1, 5, 0], [0, 1, 1]) == [2, 1, 0]
    # exact ratios: 1/3 < 2/5, a float key would also work here, a floor would not
    assert smiths_rule([2, 1], [5, 3]) == [1, 0]
    assert smiths_rule([Fraction(1, 2), Fraction(1, 3)], [1, 1]) == [1, 0]


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randrange(1, 7)
        p = [rng.randrange(0, 9) for _ in range(n)]
        w = [rng.randrange(0, 6) for _ in range(n)]
        order = smiths_rule(p, w)
        assert sorted(order) == list(range(n))
        assert weighted_completion_time(p, w, order) == brute_force(p, w)


def test_no_adjacent_swap_helps() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randrange(2, 12)
        p = [rng.randrange(1, 20) for _ in range(n)]
        w = [rng.randrange(1, 20) for _ in range(n)]
        order = smiths_rule(p, w)
        best = weighted_completion_time(p, w, order)
        for k in range(n - 1):
            o = list(order)
            o[k], o[k + 1] = o[k + 1], o[k]
            assert weighted_completion_time(p, w, o) >= best


def test_unit_weights_is_spt() -> None:
    p = [5, 1, 4, 2, 3]
    assert smiths_rule(p, [1] * 5) == sorted(range(5), key=lambda j: p[j])
