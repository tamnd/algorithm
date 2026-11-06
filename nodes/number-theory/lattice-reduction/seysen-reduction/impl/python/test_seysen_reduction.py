# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/seysen-reduction/. The authors are listed in prov/WRVXKA.jsonl.

import itertools
import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from seysen_reduction import seysen_measure, seysen_reduce, seysen_reduce_counted


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), 0)


def gram(b):
    return [[Fraction(dot(x, y)) for y in b] for x in b]


def inverse(a):
    n = len(a)
    m = [list(row) + [Fraction(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [x / piv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def det(a):
    m = [[Fraction(x) for x in row] for row in a]
    n, d = len(m), Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


def same_lattice(b, c):
    """True if c = U b with U an integer matrix of determinant +-1."""
    if len(b) != len(c):
        return False
    gi = inverse(gram(b))
    u = []
    for row in c:
        r = [Fraction(dot(row, x)) for x in b]
        coeff = [sum((r[j] * gi[j][i] for j in range(len(b))), Fraction(0)) for i in range(len(b))]
        if any(x.denominator != 1 for x in coeff):
            return False
        if [sum((coeff[i] * b[i][t] for i in range(len(b))), Fraction(0)) for t in range(len(b[0]))] != list(map(Fraction, row)):
            return False
        u.append(coeff)
    return abs(det(u)) == 1


def measure(b):
    g = gram(b)
    h = inverse(g)
    return sum((g[i][i] * h[i][i] for i in range(len(b))), Fraction(0))


def is_seysen_reduced(b):
    """No update b_j <- b_j + l b_i with integer l != 0 lowers S: |lambda*_ij| <= 1/2."""
    g = gram(b)
    h = inverse(g)
    base = measure(b)
    for i in range(len(b)):
        for j in range(len(b)):
            if i != j:
                star = (h[i][j] / h[j][j] - g[i][j] / g[i][i]) / 2
                if abs(star) > Fraction(1, 2):
                    return False
                # and directly: no small l lowers the measure
                for lam in (-2, -1, 1, 2):
                    c = [list(r) for r in b]
                    c[j] = [x + lam * y for x, y in zip(c[j], c[i])]
                    if measure(c) < base:
                        return False
    return True


def check(b):
    c, steps = seysen_reduce_counted(b)
    assert same_lattice(b, c)
    assert is_seysen_reduced(c)
    s0, s1 = measure(b), measure(c)
    assert s1 <= s0 and s1 >= len(b)
    assert seysen_measure(c) == s1
    if all(isinstance(x, int) for r in b for x in r):
        dg = det(gram(b))
        assert (s0 * dg).denominator == 1 and (s1 * dg).denominator == 1
        assert steps <= (s0 - s1) * dg
    return c, steps


def minima_2d(b):
    """lambda_1^2 and lambda_2^2 of a rank 2 lattice by a proved box search."""
    gi = inverse(gram(b))
    r2 = max(dot(u, u) for u in b)
    ranges = [range(-isqrt(floor(r2 * gi[i][i])), isqrt(floor(r2 * gi[i][i])) + 1) for i in range(2)]
    vecs = sorted(
        (dot(v, v), x)
        for x in itertools.product(*ranges)
        if any(x)
        for v in [[x[0] * b[0][t] + x[1] * b[1][t] for t in range(len(b[0]))]]
    )
    s1, x1 = vecs[0]
    s2 = next(s for s, x in vecs if x[0] * x1[1] - x[1] * x1[0] != 0)
    return s1, s2


def random_basis(rng, n, m, lo, hi):
    while True:
        b = [[rng.randint(lo, hi) for _ in range(m)] for _ in range(n)]
        if det(gram(b)) != 0:
            return b


def skew(rng, b, steps):
    b = [list(r) for r in b]
    for _ in range(steps):
        i, j = rng.sample(range(len(b)), 2)
        k = rng.choice([-3, -2, -1, 1, 2, 3])
        b[i] = [p + k * q for p, q in zip(b[i], b[j])]
    return b


def test_worked_examples():
    c, steps = check([[5, 3], [8, 5]])
    assert c == [[-1, 0], [0, -1]] and steps == 3
    assert measure([[5, 3], [8, 5]]) == 6052
    c, steps = check([[1, 1, 1], [-1, 0, 2], [3, 5, 6]])
    assert c == [[-1, 0, -1], [-2, 0, 1], [0, -1, 0]] and steps == 7
    assert measure(c) == Fraction(29, 9)


def test_dimension_one_and_empty():
    assert seysen_reduce_counted([[3, -4]]) == ([[3, -4]], 0)
    assert seysen_reduce_counted([]) == ([], 0)


def test_orthogonal_is_fixed():
    b = [[2, 0, 0], [0, 3, 0], [0, 0, 1]]
    assert seysen_reduce_counted(b) == (b, 0)
    assert seysen_measure(b) == 3


def test_nearly_dependent():
    check([[1, 0], [1000, 1]])
    check([[1, 1, 0], [1, 1, 1], [100, 101, 0]])
    check([[1, 0, 0], [0, 1, 0], [99, 100, 1]])


def test_fraction_entries():
    check([[Fraction(1, 2), Fraction(1, 3)], [Fraction(5, 4), Fraction(2, 3)]])


def test_two_dimensions_reaches_minima():
    rng = random.Random(5)
    for _ in range(150):
        b = skew(rng, random_basis(rng, 2, rng.choice([2, 3]), -9, 9), 4)
        c, _ = check(b)
        c.sort(key=lambda v: dot(v, v))
        g = gram(c)
        assert abs(g[0][1]) * 2 <= g[0][0] <= g[1][1]  # Lagrange-Gauss reduced
        assert (g[0][0], g[1][1]) == minima_2d(c)  # c is a basis of the same lattice


def test_random_bases():
    rng = random.Random(20251106)
    for n in range(2, 7):
        for _ in range(30 if n < 6 else 15):
            b = random_basis(rng, n, n + rng.randint(0, 1), -5, 5)
            if n <= 4:
                b = skew(rng, b, 3)
            check(b)


def test_errors():
    with pytest.raises(ValueError):
        seysen_reduce([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        seysen_reduce([[1, 2], [1]])
