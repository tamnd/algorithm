# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dorfler-marking/. The authors are listed in prov/G0MEX4.jsonl.

import itertools
import random
from fractions import Fraction

from dorfler_marking import dorfler_select, dorfler_sort


def brute_force_size(eta2, theta):
    goal = theta * sum(eta2)
    n = len(eta2)
    for k in range(1, n + 1):
        for s in itertools.combinations(range(n), k):
            if sum(eta2[t] for t in s) >= goal:
                return k
    return None


def check(eta2, theta, marked):
    assert len(set(marked)) == len(marked)
    assert all(0 <= t < len(eta2) for t in marked)
    assert sum(eta2[t] for t in marked) >= theta * sum(eta2)


def test_hand_example():
    eta2 = [4, 1, 9, 2, 6, 3, 5]
    assert sorted(dorfler_sort(eta2, Fraction(1, 2))) == [2, 4]
    assert sorted(dorfler_select(eta2, Fraction(1, 2))) == [2, 4]
    assert sorted(dorfler_sort(eta2, Fraction(4, 5))) == [0, 2, 4, 6]
    assert sorted(dorfler_select(eta2, Fraction(4, 5))) == [0, 2, 4, 6]
    assert len(dorfler_sort(eta2, 1)) == 7


def test_minimal_against_brute_force_exact():
    rng = random.Random(2024)
    for _ in range(300):
        n = rng.randint(1, 9)
        eta2 = [Fraction(rng.randint(0, 12), rng.randint(1, 4)) for _ in range(n)]
        if sum(eta2) == 0:
            eta2[0] = Fraction(1)
        theta = Fraction(rng.randint(1, 10), 10)
        best = brute_force_size(eta2, theta)
        a = dorfler_sort(eta2, theta)
        b = dorfler_select(eta2, theta, random.Random(rng.randint(0, 10 ** 6)))
        check(eta2, theta, a)
        check(eta2, theta, b)
        assert len(a) == best
        assert len(b) == best


def test_same_size_on_large_float_input_with_ties():
    rng = random.Random(9)
    eta2 = [float(rng.randint(0, 50)) for _ in range(5000)]  # integers: sums are exact
    for theta in (0.1, 0.3, 0.5, 0.9, 1.0):
        a = dorfler_sort(eta2, theta)
        b = dorfler_select(eta2, theta, random.Random(1))
        check(eta2, theta, a)
        check(eta2, theta, b)
        assert len(a) == len(b)
        rest = set(range(len(eta2))) - set(b)
        if rest:
            assert min(eta2[t] for t in b) >= max(eta2[t] for t in rest)  # b holds the largest values


def test_all_zero_and_single():
    assert len(dorfler_sort([0.0, 0.0, 0.0], 0.5)) == 1
    assert len(dorfler_select([0.0, 0.0, 0.0], 0.5)) == 1
    assert dorfler_sort([2.0], 1.0) == [0]
    assert dorfler_select([2.0], 1.0) == [0]
