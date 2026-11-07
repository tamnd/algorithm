# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kronecker-factorization-method/. The authors are listed in prov/9JH5VC.jsonl.

import random
from fractions import Fraction
from math import gcd

import pytest

from kronecker_factorization_method import divisors, evaluate, exact_quotient, interpolate, kronecker_factor


def mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r


def primitive(f):
    c = 0
    for a in f:
        c = gcd(c, a)
    if f[-1] < 0:
        c = -c
    return [a // c for a in f]


def has_rational_root(f):
    """Rational root test: a root p/q has p | a_0 and q | lc."""
    if f[0] == 0:
        return True
    for p in divisors(f[0]):
        for q in divisors(f[-1]):
            for s in (1, -1):
                r = Fraction(s * p, q)
                if sum(c * r ** i for i, c in enumerate(f)) == 0:
                    return True
    return False


def check(f):
    fs = kronecker_factor(f)
    prod = [1]
    for g in fs:
        assert g[-1] > 0 and len(g) >= 2
        prod = mul(prod, g)
    assert prod == f
    for g in fs:
        if len(g) - 1 in (2, 3):  # degree 2 or 3: irreducible iff no rational root
            assert not has_rational_root(g)
    return fs


def test_worked_example():
    assert check([4, 0, 0, 0, 1]) == [[2, -2, 1], [2, 2, 1]]  # x^4 + 4


def test_known_factorizations():
    assert sorted(check([-1, 0, 0, 0, 0, 0, 1])) == sorted([[-1, 1], [1, 1], [1, -1, 1], [1, 1, 1]])
    assert check([1, 0, 1]) == [[1, 0, 1]]
    assert check([-2, 0, 1]) == [[-2, 0, 1]]
    assert check([1, 1, 1, 1, 1]) == [[1, 1, 1, 1, 1]]  # cyclotomic, irreducible
    assert check([0, 1]) == [[0, 1]]
    assert check([0, 0, 0, 1]) == [[0, 1], [0, 1], [0, 1]]
    assert check([1, 2, 1]) == [[1, 1], [1, 1]]
    assert check([3, 2]) == [[3, 2]]
    assert kronecker_factor([1]) == []


def test_random_products():
    rng = random.Random(1882)
    for _ in range(500):
        f = [1]
        for _ in range(rng.randint(1, 3)):
            deg = rng.randint(1, 2)
            g = [rng.randint(-3, 3) for _ in range(deg + 1)]
            if g[-1] == 0:
                g[-1] = 1
            f = mul(f, g)
        f = primitive(f)
        check(f)


def test_interpolation_and_division():
    rng = random.Random(5)
    for _ in range(500):
        g = [rng.randint(-5, 5) for _ in range(rng.randint(1, 4))] + [rng.randint(1, 3)]
        pts = list(range(-2, len(g) - 2))
        assert interpolate(pts, [evaluate(g, a) for a in pts]) == g
        h = [rng.randint(-3, 3) for _ in range(3)] + [1]
        assert exact_quotient(mul(g, h), g) == h


def test_bad_input():
    with pytest.raises(ValueError):
        kronecker_factor([2, 4])
    with pytest.raises(ValueError):
        kronecker_factor([1, -1])
