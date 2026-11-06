# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lll-algorithm/. The authors are listed in prov/82SX9W.jsonl.

import itertools
import random
from fractions import Fraction
from math import floor, isqrt

import pytest

from lll_algorithm import lll_reduce, lll_reduce_counted

HALF = Fraction(1, 2)


def dot(u, v):
    return sum((a * b for a, b in zip(u, v)), 0)


def gram(b):
    return [[Fraction(dot(x, y)) for y in b] for x in b]


def inverse(a):
    """Exact inverse of a square Fraction matrix by Gauss-Jordan elimination."""
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
    """Exact determinant by fraction-valued Gaussian elimination."""
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


def gso(b):
    """Gram-Schmidt from scratch: returns (mu, B) with B[i] = ||b_i*||^2."""
    n = len(b)
    star, mu, big = [], [[Fraction(0)] * n for _ in range(n)], []
    for i in range(n):
        v = [Fraction(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = Fraction(dot(b[i], star[j])) / big[j]
            v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
        star.append(v)
        big.append(dot(v, v))
    return mu, big


def same_lattice(b, c):
    """True if the rows of c are a basis of L(b): c = U b with U integer, det U = +-1."""
    if len(b) != len(c):
        return False
    gi = inverse(gram(b))
    u = []
    for row in c:
        r = [Fraction(dot(row, x)) for x in b]
        coeff = [sum((r[j] * gi[j][i] for j in range(len(b))), Fraction(0)) for i in range(len(b))]
        if any(x.denominator != 1 for x in coeff):
            return False
        combo = [sum((coeff[i] * b[i][t] for i in range(len(b))), Fraction(0)) for t in range(len(row))]
        if combo != [Fraction(x) for x in row]:
            return False
        u.append(coeff)
    return abs(det(u)) == 1


def is_lll_reduced(b, delta):
    mu, big = gso(b)
    n = len(b)
    if any(abs(mu[i][j]) > HALF for i in range(n) for j in range(i)):
        return False
    return all(delta * big[k - 1] <= big[k] + mu[k][k - 1] ** 2 * big[k - 1] for k in range(1, n))


def shortest_sq(b):
    """lambda_1^2 by enumeration of all coefficient vectors in a box that is proved large enough.

    Any v = x b with ||v||^2 <= R2 = min ||b_i||^2 has |x_i| <= sqrt(R2 * (G^-1)_ii),
    by Cauchy-Schwarz with the dual basis vector d_i, whose squared length is (G^-1)_ii.
    """
    g = gram(b)
    gi = inverse(g)
    r2 = min(g[i][i] for i in range(len(b)))
    box = [isqrt(floor(r2 * gi[i][i])) for i in range(len(b))]
    best = r2
    for x in itertools.product(*[range(-t, t + 1) for t in box]):
        if any(x):
            v = [sum((x[i] * b[i][t] for i in range(len(b))), 0) for t in range(len(b[0]))]
            best = min(best, dot(v, v))
    return best


def potential(b):
    """D = product over i < n of d_i, d_i = product of B_1..B_i (an integer for integer b)."""
    _, big = gso(b)
    d, acc = Fraction(1), Fraction(1)
    for i in range(len(b) - 1):
        acc *= big[i]
        d *= acc
    return d


def test_worked_example():
    out, swaps = lll_reduce_counted([[1, 1, 1], [-1, 0, 2], [3, 5, 6]])
    assert out == [[0, 1, 0], [1, 0, 1], [-2, 0, 1]]
    assert swaps == 2
    assert gso(out)[1] == [1, 2, Fraction(9, 2)]


def test_dimension_one():
    assert lll_reduce([[-7, 3]]) == [[-7, 3]]
    assert lll_reduce([[5]]) == [[5]]


def test_empty_basis():
    assert lll_reduce([]) == []


def test_already_reduced_is_unchanged():
    for b in ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [[0, 1, 0], [1, 0, 1], [-2, 0, 1]], [[2, 0], [-1, 2]]):
        out, swaps = lll_reduce_counted(b)
        assert out == b and swaps == 0


def test_nearly_dependent():
    b = [[1, 0, 0], [1000, 1, 0], [999, 1, 1]]
    out = lll_reduce(b)
    assert same_lattice(b, out) and is_lll_reduced(out, Fraction(3, 4))
    c = [[100001, 100000], [100000, 99999]]
    out = lll_reduce(c)
    assert same_lattice(c, out) and is_lll_reduced(out, Fraction(3, 4))
    assert sorted(dot(v, v) for v in out) == [1, 1]


def test_fraction_input_and_delta():
    b = [[Fraction(1, 2), Fraction(1, 3)], [Fraction(5, 7), 2]]
    for delta in (Fraction(1, 2), Fraction(3, 4), Fraction(99, 100)):
        out = lll_reduce(b, delta)
        assert same_lattice(b, out) and is_lll_reduced(out, delta)


def test_errors():
    with pytest.raises(ValueError):
        lll_reduce([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        lll_reduce([[1, 2], [3]])
    with pytest.raises(ValueError):
        lll_reduce([[1, 0], [0, 1]], Fraction(1, 4))
    with pytest.raises(ValueError):
        lll_reduce([[1, 0], [0, 1]], 1)


def random_basis(rng, n, m, size):
    while True:
        b = [[rng.randint(-size, size) for _ in range(m)] for _ in range(n)]
        if det(gram(b)) != 0:
            return b


def test_random_against_oracles():
    rng = random.Random(20251106)
    for trial in range(150):
        n = rng.randint(2, 6)
        m = n + rng.randint(0, 2)
        size = rng.choice([3, 20, 200])
        b = random_basis(rng, n, m, size)
        if trial % 5 == 0:  # a skewed basis: add big multiples of the first row
            b = [b[0]] + [[x + rng.randint(-50, 50) * y for x, y in zip(row, b[0])] for row in b[1:]]
        delta = rng.choice([Fraction(1, 2), Fraction(3, 4), Fraction(99, 100)])
        out, swaps = lll_reduce_counted(b, delta)
        assert same_lattice(b, out)
        assert is_lll_reduced(out, delta)
        alpha = 1 / (delta - Fraction(1, 4))
        n1 = dot(out[0], out[0])
        assert n1 <= alpha ** (n - 1) * shortest_sq(out)
        assert n1 ** n <= alpha ** (n * (n - 1) // 2) * det(gram(b))
        # each swap multiplies the integer potential by less than delta
        assert potential(out) <= delta ** swaps * potential(b)
        assert potential(out) >= 1


def test_dimension_two_with_delta_near_one_finds_minimum():
    rng = random.Random(7)
    for _ in range(100):
        b = random_basis(rng, 2, 2, 30)
        out = lll_reduce(b, Fraction(999, 1000))
        # with delta close to 1, a reduced 2D basis has ||b1||^2 <= ||b2||^2 / delta
        assert dot(out[0], out[0]) * Fraction(999, 1000) <= dot(out[1], out[1])
        assert dot(out[0], out[0]) <= Fraction(1000, 999) * shortest_sq(out)
