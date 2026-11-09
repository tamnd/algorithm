# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/epsilon-indicator/. The authors are listed in prov/56A304.jsonl.

import random
from fractions import Fraction

from epsilon_indicator import better, eps_additive, eps_multiplicative, weakly_dominates_set

A = [(1, 4), (2, 2), (4, 1)]
B = [(1, 4), (3, 3), (4, 1)]


def test_hand_values() -> None:
    assert eps_additive(A, B) == 0
    assert eps_additive(B, A) == 1
    assert better(A, B) and not better(B, A)
    # incomparable sets
    assert eps_additive([(0, 2)], [(1, 1)]) == 1 and eps_additive([(1, 1)], [(0, 2)]) == 1
    assert eps_multiplicative([(2, 4)], [(4, 2)]) == 2
    assert eps_multiplicative(B, A) == Fraction(3, 2)


def rand_set(rng, p, k, hi=6):
    return [tuple(rng.randint(0, hi) for _ in range(p)) for _ in range(k)]


def test_sign_decides_weak_dominance() -> None:
    rng = random.Random(1)
    for _ in range(3000):
        p = rng.randint(1, 4)
        a, b = rand_set(rng, p, rng.randint(1, 4)), rand_set(rng, p, rng.randint(1, 4))
        assert (eps_additive(a, b) <= 0) == weakly_dominates_set(a, b)
        e = eps_additive(a, b)
        # e is the smallest shift: a - e weakly dominates b, a - (e - 1/2) does not
        shifted = [tuple(u - e for u in x) for x in a]
        assert weakly_dominates_set(shifted, b)
        shifted = [tuple(u - e + Fraction(1, 2) for u in x) for x in a]
        assert not weakly_dominates_set(shifted, b)


def test_triangle_inequality() -> None:
    rng = random.Random(2)
    for _ in range(2000):
        p = rng.randint(1, 3)
        a, b, c = (rand_set(rng, p, rng.randint(1, 4)) for _ in range(3))
        assert eps_additive(a, c) <= eps_additive(a, b) + eps_additive(b, c)


def test_unary_weak_compliance_and_no_strictness() -> None:
    rng = random.Random(3)
    for _ in range(2000):
        p = rng.randint(2, 3)
        ref = rand_set(rng, p, rng.randint(1, 5))
        a = rand_set(rng, p, rng.randint(1, 4))
        b = [tuple(u + rng.randint(0, 2) for u in rng.choice(a)) for _ in range(rng.randint(1, 4))]
        assert eps_additive(a, ref) <= eps_additive(b, ref)
    ref = [(0, 10), (10, 0)]
    a, b = [(0, 10), (10, 0), (5, 5)], [(0, 10), (10, 0)]
    assert better(a, b)
    assert eps_additive(a, ref) == eps_additive(b, ref) == 0
