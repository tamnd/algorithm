# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pslq-algorithm/. The authors are listed in prov/GH5331.jsonl.

import itertools
import random
from fractions import Fraction
from math import gcd, isqrt

import pytest

from pslq_algorithm import pslq, pslq_counted


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), 0)


def shortest_relation_sq(x, bound_sq):
    """min ||m||^2 over nonzero integer m with <m, x> = 0 and ||m||^2 <= bound_sq.

    Every such m has |m_i| <= isqrt(bound_sq), so the box search is exhaustive.
    """
    c = isqrt(bound_sq)
    best = None
    for m in itertools.product(range(-c, c + 1), repeat=len(x)):
        if any(m) and dot(m, x) == 0:
            s = dot(m, m)
            if s <= bound_sq and (best is None or s < best):
                best = s
    return best


def integer_scale(x):
    """The primitive integer vector on the line of x (same relations)."""
    x = [Fraction(v) for v in x]
    den = 1
    for v in x:
        den = den * v.denominator // gcd(den, v.denominator)
    z = [int(v * den) for v in x]
    g = 0
    for v in z:
        g = gcd(g, v)
    return [v // g for v in z]


def check(x, gamma2=Fraction(2), brute_limit=40000):
    m, iterations, bounds = pslq_counted(x, gamma2)
    assert any(m) and dot(m, x) == 0
    s = dot(m, m)
    # max_j ||p_j*||^2 never increases, and starts at most 1
    assert all(b2 <= b1 for b1, b2 in zip(bounds, bounds[1:]))
    assert all(b <= 1 for b in bounds)
    # the iteration bound: tau^(2 I) <= ||x||^(2 (n - 1)) for the primitive integer x
    tau2 = 4 * gamma2 / (4 + gamma2)
    z = integer_scale(x)
    assert tau2 ** iterations <= dot(z, z) ** (len(x) - 1)
    if (2 * isqrt(s) + 1) ** len(x) <= brute_limit:
        best = shortest_relation_sq(x, s)
        assert best is not None and best <= s
        # the lower bound of every iteration: ||r||^2 >= 1 / max_j ||p_j*||^2
        assert all(best * b >= 1 for b in bounds)
    return m, iterations


def test_worked_example():
    m, iterations, bounds = pslq_counted([3, 5, 7])
    assert m == [-1, 2, -1] and iterations == 3
    assert bounds == [Fraction(74, 83), Fraction(74, 83), Fraction(22, 83)]
    check([3, 5, 7])


def test_not_always_shortest():
    x = [Fraction(-5, 2), -6, -7]
    m = pslq(x)
    assert m == [0, 7, -6]
    assert shortest_relation_sq(x, dot(m, m)) == 9
    assert dot([2, -2, 1], x) == 0


def test_two_numbers():
    m = pslq([355, -113])
    assert m in ([113, 355], [-113, -355])
    rng = random.Random(1)
    for _ in range(100):
        p, q = rng.randint(-500, 500), rng.randint(1, 500)
        if p == 0:
            continue
        m = pslq([Fraction(p, q), 1])
        g = gcd(p, q)
        assert m in ([q // g, -p // g], [-q // g, p // g])


def test_zero_entries():
    assert pslq([0, 4, 5]) == [1, 0, 0]
    assert pslq([2, 3, 0]) == [0, 0, 1]
    assert pslq_counted([1, 1])[0] in ([1, -1], [-1, 1])


def test_known_relation():
    # x = (1, 1/2, 1/3, 1/4): many small relations, PSLQ must return a short one
    check([1, Fraction(1, 2), Fraction(1, 3), Fraction(1, 4)])
    check([12, 18, 30, 42, 66])


def test_hard_rational_approximation():
    # close to (1, sqrt 2, sqrt 3): only long relations exist
    x = [1, Fraction(14142136, 10**7), Fraction(17320508, 10**7)]
    m, iterations, bounds = pslq_counted(x)
    assert all(dot(m, m) * b >= 1 for b in bounds)
    check(x)


def test_random_vectors():
    rng = random.Random(20251106)
    for n in range(2, 7):
        for _ in range(40 if n <= 4 else 12):
            hi = 30 if n <= 4 else 6
            x = [Fraction(rng.randint(-hi, hi), rng.randint(1, 4)) for _ in range(n)]
            if not any(x):
                continue
            check(x)


def test_other_gamma():
    rng = random.Random(9)
    for gamma2 in (Fraction(3, 2), Fraction(4)):
        for _ in range(30):
            x = [rng.randint(-40, 40) for _ in range(rng.randint(2, 4))]
            if any(x):
                check(x, gamma2)


def test_errors():
    with pytest.raises(ValueError):
        pslq([5])
    with pytest.raises(ValueError):
        pslq([0, 0, 0])
    with pytest.raises(ValueError):
        pslq([1, 2], Fraction(4, 3))
