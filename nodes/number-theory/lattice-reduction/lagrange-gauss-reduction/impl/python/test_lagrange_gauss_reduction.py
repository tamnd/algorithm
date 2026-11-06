# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lagrange-gauss-reduction/. The authors are listed in prov/TQ44SE.jsonl.

import itertools
import random
from fractions import Fraction
from math import isqrt

import pytest

from lagrange_gauss_reduction import lagrange_gauss_reduce


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), 0)


def same_lattice(b, c):
    """True if the rows of c are a basis of the lattice with basis rows b (rank 2).

    Solves c = U b exactly with the Gram matrix and checks that U is an integer
    matrix with determinant +1 or -1.
    """
    g11, g12, g22 = dot(b[0], b[0]), dot(b[0], b[1]), dot(b[1], b[1])
    det = Fraction(g11 * g22 - g12 * g12)
    u = []
    for row in c:
        r1, r2 = dot(row, b[0]), dot(row, b[1])
        x = (r1 * g22 - r2 * g12) / det
        y = (r2 * g11 - r1 * g12) / det
        if x.denominator != 1 or y.denominator != 1:
            return False
        if [x * p + y * q for p, q in zip(b[0], b[1])] != list(row):
            return False
        u.append((int(x), int(y)))
    return abs(u[0][0] * u[1][1] - u[0][1] * u[1][0]) == 1


def minima_brute(b):
    """(lambda_1^2, lambda_2^2) by search over a coefficient box that is proved large enough.

    For a lattice vector x1 b1 + x2 b2 of norm at most R, |x_i| <= R ||d_i||, where
    d_1, d_2 is the dual basis (Cauchy-Schwarz on x_i = <v, d_i>). R^2 is the larger
    of the two squared norms, which bounds lambda_2^2.
    """
    g11, g12, g22 = dot(b[0], b[0]), dot(b[0], b[1]), dot(b[1], b[1])
    det = Fraction(g11 * g22 - g12 * g12)
    r2 = max(g11, g22)
    # ||d_1||^2 = g22 / det and ||d_2||^2 = g11 / det
    k1 = isqrt(int(r2 * g22 / det)) + 1
    k2 = isqrt(int(r2 * g11 / det)) + 1
    vecs = []
    for x1, x2 in itertools.product(range(-k1, k1 + 1), range(-k2, k2 + 1)):
        if (x1, x2) != (0, 0):
            v = [x1 * p + x2 * q for p, q in zip(b[0], b[1])]
            vecs.append((dot(v, v), (x1, x2)))
    vecs.sort()
    l1, s = vecs[0]
    l2 = min(n for n, x in vecs if x[0] * s[1] - x[1] * s[0] != 0)
    return l1, l2


def check(b1, b2):
    u, v = lagrange_gauss_reduce(b1, b2)
    assert same_lattice([b1, b2], [u, v])
    assert dot(u, u) <= dot(v, v)
    assert 2 * abs(dot(u, v)) <= dot(u, u)
    l1, l2 = minima_brute([u, v])
    assert dot(u, u) == l1
    assert dot(v, v) == l2
    return u, v


def test_example():
    u, v = lagrange_gauss_reduce([24, 60], [21, 53])
    assert (u, v) == ([3, -1], [0, 4])
    check([24, 60], [21, 53])


def test_already_reduced_is_kept():
    assert lagrange_gauss_reduce([1, 0], [0, 1]) == ([1, 0], [0, 1])
    assert lagrange_gauss_reduce([3, -1], [0, 4]) == ([3, -1], [0, 4])
    # mu = 1/2 exactly: the result is still reduced, and has the same lengths
    u, v = lagrange_gauss_reduce([2, 0], [1, 5])
    assert dot(u, u) == 4 and dot(v, v) == 26
    check([2, 0], [1, 5])


def test_order_of_input():
    for b1, b2 in (([5, 1], [1, 0]), ([0, 7], [3, 0]), ([1, 1, 1], [1, 0, 0])):
        check(b1, b2)


def test_nearly_dependent():
    rng = random.Random(77)
    for _ in range(300):
        m = rng.randint(2, 6)
        a = [rng.randint(-9, 9) for _ in range(m)]
        if not any(a):
            continue
        k = rng.randint(-40, 40)
        e = [0] * m
        e[rng.randrange(m)] = rng.choice([-1, 1])
        b = [k * x + y for x, y in zip(a, e)]
        if dot(a, a) * dot(b, b) == dot(a, b) ** 2:
            continue
        check(a, b)


def test_rational_entries():
    check([Fraction(1, 2), Fraction(3, 7)], [Fraction(5, 3), Fraction(-2, 9)])
    check([Fraction(10, 3), 7, 1], [3, Fraction(13, 2), 1])


def test_dependent_raises():
    with pytest.raises(ValueError):
        lagrange_gauss_reduce([1, 2], [2, 4])
    with pytest.raises(ValueError):
        lagrange_gauss_reduce([0, 0], [1, 0])
    with pytest.raises(ValueError):
        lagrange_gauss_reduce([1, 2], [1, 2, 3])


def test_random_against_brute_force():
    rng = random.Random(2024)
    done = 0
    while done < 1500:
        m = rng.randint(2, 6)
        span = rng.choice([3, 20, 200])
        b1 = [rng.randint(-span, span) for _ in range(m)]
        b2 = [rng.randint(-span, span) for _ in range(m)]
        if dot(b1, b1) * dot(b2, b2) == dot(b1, b2) ** 2:
            continue
        check(b1, b2)
        done += 1


def test_large_entries():
    rng = random.Random(9)
    for _ in range(200):
        b1 = [rng.randint(-(2**62), 2**62) for _ in range(2)]
        b2 = [rng.randint(-(2**62), 2**62) for _ in range(2)]
        if b1[0] * b2[1] == b1[1] * b2[0]:
            continue
        u, v = lagrange_gauss_reduce(b1, b2)
        assert same_lattice([b1, b2], [u, v])
        assert dot(u, u) <= dot(v, v) and 2 * abs(dot(u, v)) <= dot(u, u)
