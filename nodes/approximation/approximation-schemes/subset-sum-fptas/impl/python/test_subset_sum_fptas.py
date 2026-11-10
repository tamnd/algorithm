# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subset-sum-fptas/. The authors are listed in prov/MWFG11.jsonl.

import itertools
import math
import random
from fractions import Fraction

from subset_sum_fptas import approx_subset_sum, trim, trimmed_lists


def brute_force(x: list[int], t: int) -> int:
    best = 0
    for r in range(len(x) + 1):
        for c in itertools.combinations(x, r):
            if best < sum(c) <= t:
                best = sum(c)
    return best


def values(x: list[int], t: int, eps: Fraction) -> list[list[int]]:
    return [[v for v, _ in lst] for lst in trimmed_lists(x, t, eps)]


def test_example() -> None:
    x = [29, 34, 36, 42, 46]
    assert values(x, 82, Fraction(1)) == [
        [0, 29],
        [0, 29, 34, 63],
        [0, 29, 34, 63, 70],
        [0, 29, 34, 42, 63, 70],
        [0, 29, 34, 42, 63, 70, 80],
    ]
    assert approx_subset_sum(x, 82, 1) == (80, [1, 4])
    assert brute_force(x, 82) == 82


def test_clrs_example() -> None:
    # Cormen et al., Section 35.5: the result is 302, the optimum is 307
    x = [104, 102, 201, 101]
    assert values(x, 308, Fraction(2, 5))[-1] == [0, 101, 201, 302]
    assert approx_subset_sum(x, 308, Fraction(2, 5)) == (302, [2, 3])
    assert brute_force(x, 308) == 307


def test_trim() -> None:
    lst = [(v, None) for v in [10, 11, 12, 15, 20, 21, 22, 23, 29]]
    assert [v for v, _ in trim(lst, Fraction(1, 10))] == [10, 12, 15, 20, 23, 29]


def test_edges() -> None:
    assert approx_subset_sum([], 10, Fraction(1, 2)) == (0, [])
    assert approx_subset_sum([5, 7], 3, Fraction(1, 2)) == (0, [])
    assert approx_subset_sum([5], 5, Fraction(1, 2)) == (5, [0])
    assert approx_subset_sum([3, 3, 3], 0, Fraction(1, 2)) == (0, [])
    for bad in (0, -1, 2):
        try:
            approx_subset_sum([1], 1, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("eps out of range was accepted")


def test_ratio_and_list_size() -> None:
    rng = random.Random(2025)
    for _ in range(400):
        n = rng.randint(1, 9)
        x = [rng.randint(1, 200) for _ in range(n)]
        t = rng.randint(1, 600)
        opt = brute_force(x, t)
        for eps in (Fraction(1), Fraction(1, 2), Fraction(1, 5), Fraction(1, 20)):
            z, chosen = approx_subset_sum(x, t, eps)
            assert len(set(chosen)) == len(chosen)
            assert z == sum(x[i] for i in chosen) <= t
            assert z * (1 + eps) >= opt
            assert z >= (1 - eps) * opt
            delta = eps / (2 * n)
            for lst in values(x, t, eps):
                assert lst[0] == 0 and lst == sorted(set(lst)) and lst[-1] <= t
                # a strict chain y_k > (1 + delta) y_(k-1) of positive values at most t
                assert len(lst) <= 2 or (1 + delta) ** (len(lst) - 2) < t
                assert len(lst) <= 3 * n * math.log(max(t, 1)) / eps + 2


def test_small_eps_is_exact() -> None:
    rng = random.Random(9)
    for _ in range(200):
        n = rng.randint(1, 8)
        x = [rng.randint(1, 50) for _ in range(n)]
        t = rng.randint(1, 150)
        # eps < 1 / t makes OPT / (1 + eps) > OPT - 1, so the result is exact
        z, _ = approx_subset_sum(x, t, Fraction(1, t + 1))
        assert z == brute_force(x, t)
